import logging

from openai.types.shared_params import ChatModel

from dict8.llm.client import get_openai_client
from dict8.utils import load_prompt

logger = logging.getLogger(__name__)

BASE_INSTRUCTIONS = load_prompt("blog_writer.md")

MODEL: ChatModel = "gpt-5-mini"


async def write_blog(ctx_files: dict[int, str]) -> str:
    """Produce a complete blog post from the phase context files.

    *ctx_files* maps phase numbers (1-4) to the content of each
    ``phase{N}ctx.md`` file.  Returns the final blog markdown or an error
    string starting with ``Error:``.
    """
    parts: list[str] = []
    for phase in sorted(ctx_files):
        parts.append(f"--- PHASE {phase} CONTEXT ---\n\n{ctx_files[phase]}\n")
    user_content = "\n".join(parts)

    try:
        client = get_openai_client()
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": BASE_INSTRUCTIONS},
                {"role": "user", "content": user_content},
            ],
        )
        text = (response.choices[0].message.content or "").strip()
        if not text:
            return "Error: Blog writer returned empty output."

        return text
    except Exception as e:
        logger.exception("Blog writing failed")
        return f"Error: {type(e).__name__}: {e}"
