"""
Text-only research agent for LiveKit. No STT/TTS. Called by the voice agent's
research tool. Uses Tavily for web search and a direct LLM+tools loop.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

import httpx
from livekit.agents import NOT_GIVEN, Agent, function_tool, inference
from livekit.agents import llm as llm_module
from livekit.agents.llm import ChatContext, ToolContext, execute_function_call

TAVILY_SEARCH_URL = "https://api.tavily.com/search"
TAVILY_TIMEOUT_S = 15.0
RESEARCH_TIMEOUT_S = 30.0
MAX_RESULTS = 5
MAX_RESEARCH_ITERATIONS = 5

RESEARCH_INSTRUCTIONS = """
You are a research agent. Answer questions accurately using the web_search tool.
Do not invent facts. Base answers only on tool results. Be concise and factual.
""".strip()


@function_tool()
async def web_search(query: str) -> str:
    """Search the web for current, factual information. Returns formatted title+summary per result."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY is not set."

    payload: dict[str, Any] = {
        "query": query,
        "max_results": MAX_RESULTS,
        "search_depth": "basic",
        "include_answer": False,
    }

    try:
        async with httpx.AsyncClient(timeout=TAVILY_TIMEOUT_S) as client:
            response = await client.post(
                TAVILY_SEARCH_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
            )
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException:
        return "Error: Web search timed out."
    except httpx.HTTPStatusError as e:
        return f"Error: Search failed ({e.response.status_code})."
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"

    results = data.get("results") or []
    if not results:
        return "No results found."

    lines: list[str] = []
    for i, item in enumerate(results, start=1):
        title = item.get("title") or "No title"
        content = (item.get("content") or "").strip()
        lines.append(f"{i}. {title}\n   {content}")

    return "\n\n".join(lines)


RESEARCH_AGENT = Agent(
    id="research_agent",
    instructions=RESEARCH_INSTRUCTIONS,
    tools=[web_search],
    stt=None,
    tts=None,
    llm=inference.LLM.from_model_string("openai/gpt-4.1-mini"),
)


def _merge_tool_calls(
    tool_calls: list[llm_module.FunctionToolCall],
) -> list[llm_module.FunctionToolCall]:
    """Merge streamed tool calls by call_id."""
    by_id: dict[str, list[llm_module.FunctionToolCall]] = {}
    order: list[str] = []
    for tc in tool_calls:
        cid = tc.call_id
        if cid not in by_id:
            order.append(cid)
            by_id[cid] = []
        by_id[cid].append(tc)
    merged = []
    for cid in order:
        parts = by_id[cid]
        name = next((p.name for p in parts if p.name), "")
        arguments = "".join(p.arguments or "" for p in parts)
        merged.append(
            llm_module.FunctionToolCall(
                call_id=cid,
                name=name,
                arguments=arguments,
                extra=parts[-1].extra if parts else None,
            )
        )
    return merged


async def run_research(query: str) -> str:
    """Run research (LLM + tools loop, no session). Returns answer text or error string."""
    agent = RESEARCH_AGENT
    if agent.llm is None or agent.llm is NOT_GIVEN:
        return "Error: Research agent has no LLM configured."
    if not isinstance(agent.llm, llm_module.LLM):
        return "Error: Research agent LLM is not a chat LLM."
    llm_node = agent.llm
    tool_ctx = ToolContext(agent.tools)
    tools = tool_ctx.flatten()

    ctx = ChatContext()
    ctx.add_message(role="system", content=agent.instructions)
    ctx.add_message(role="user", content=query)

    try:
        for _ in range(MAX_RESEARCH_ITERATIONS):
            stream = llm_node.chat(chat_ctx=ctx, tools=tools, tool_choice="auto")
            response = await asyncio.wait_for(
                stream.collect(), timeout=RESEARCH_TIMEOUT_S
            )

            merged_calls = (
                _merge_tool_calls(response.tool_calls) if response.tool_calls else []
            )

            if not merged_calls:
                return response.text.strip() or "I couldn't find an answer."

            ctx.add_message(role="assistant", content=response.text or "")
            for tc in merged_calls:
                result = await execute_function_call(tc, tool_ctx, call_ctx=None)
                ctx.insert(result.fnc_call)
                if result.fnc_call_out is not None:
                    ctx.insert(result.fnc_call_out)

        return "Error: Too many tool call rounds."
    except asyncio.TimeoutError:
        return "Error: Research timed out."
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"
