import random
from abc import ABC, abstractmethod

from livekit.agents import Agent, RunContext, function_tool
from livekit.agents.beta.tools.end_call import EndCallTool
from livekit.agents.llm import ChatContext
from livekit.plugins import cartesia

from dict8 import projects
from dict8.agents.research_agent import run_research
from dict8.utils import load_prompt

BASE_INSTRUCTIONS = load_prompt("sys.md")

# Cartesia TTS speech speed (0.6–2.0). Lower = slower, more natural for conversation.
TTS_SPEED = 0.93

TRANSFER_MESSAGES = [
    "Just a second please, I'm going to transfer you to our {name}.",
    "One moment, I'll send you over to our {name}.",
    "Hold on a sec, I'm connecting you with our {name}.",
    "Give me just a second. I'm transferring you to our {name}.",
]

RESEARCH_INTRO_PHRASES = [
    "I googled it and ",
    "I searched it up and ",
    "I looked it up and ",
    "I checked and ",
    "I ran a quick search and ",
]


@function_tool()
async def create_new_project(slug: str, name: str, description: str) -> str:
    """Create a new blog project and set it active. Slug: URL-friendly (e.g. my-blog-topic). Name: display title. Description: brief, disambiguating summary for model context (e.g. 'Navy SEALs training' vs 'Pet seal care'). Do not announce to the author."""
    try:
        proj = projects.create_project(slug, name, description)
        projects.set_active_project(proj.id)
        return f"Created and active. Id: {proj.id}"
    except ValueError as e:
        return str(e)


@function_tool()
async def list_projects() -> str:
    """List projects (id, name, slug, description). Use to find a project by topic when resuming. Do not announce to the author."""
    items = projects.list_projects()
    if not items:
        return "No projects yet. Use create_new_project to create one."
    lines = [f"- {p.name} (id: {p.id}, slug: {p.slug}): {p.description}" for p in items]
    return "\n".join(lines)


@function_tool()
async def set_active_project(project_id: str) -> str:
    """Set the active project by id. Phase context and blog reads/writes use this project. Do not announce to the author."""
    try:
        projects.set_active_project(project_id)
        proj = projects.get_active_project()
        if proj is None:
            return "No active project. Use list_projects and set_active_project first."
        return f"Active project is now '{proj.name}' (id: {proj.id})."
    except ValueError as e:
        return str(e)


@function_tool()
async def get_project_context(phase: int) -> str:
    """Get persisted markdown context for phase 1–4 from the active project. Use when resuming or before updating that phase's context."""
    proj = projects.get_active_project()
    if proj is None:
        return "No active project. Use list_projects and set_active_project first."
    return (
        proj.get_context_for_phase(phase) or f"No context saved yet for phase {phase}."
    )


@function_tool()
async def get_blog_content() -> str:
    """Get the current blog markdown from the active project."""
    proj = projects.get_active_project()
    if proj is None:
        return "No active project. Use list_projects and set_active_project first."
    return proj.get_blog() or "No blog content saved yet."


@function_tool()
async def save_project_context(phase: int, content: str) -> str:
    """Save markdown for phase 1–4 to the active project. Content is LLM-facing: detailed, technical, comprehensive. Update regularly as the conversation progresses. Do not announce to the author."""
    proj = projects.get_active_project()
    if proj is None:
        return "No active project. Use list_projects and set_active_project first."
    proj.set_context_for_phase(phase, content)
    return f"Saved context for phase {phase}."


@function_tool()
async def save_blog_content(content: str) -> str:
    """Save the full blog markdown to the active project. Overwrites existing. Do not announce to the author."""
    proj = projects.get_active_project()
    if proj is None:
        return "No active project. Use list_projects and set_active_project first."
    proj.set_blog(content)
    return "Blog content saved."


@function_tool()
async def research(context: RunContext, query: str) -> str:
    """Look up factual information on the web. You MUST call this tool whenever the author asks a fact question (who, when, what, current events, names, dates) or asks you to research/look something up. Never answer factual questions from memory—always call this tool first. When you tell the author the result, you MUST say the exact opening phrase at the start of this tool's return (e.g. 'I googled it and', 'I looked it up and') before the finding. Never omit that phrase."""
    raw = await run_research(query)
    if not raw or raw.startswith("Error"):
        return raw
    intro = random.choice(RESEARCH_INTRO_PHRASES)
    start = f"{raw[0].lower()}{raw[1:]}" if raw[0].isupper() else raw
    return f"{intro}{start}"


class BasePhaseAgent(ABC, Agent):
    phase: int
    name: str
    _REGISTRY: dict[int, type["BasePhaseAgent"]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "phase"):
            BasePhaseAgent._REGISTRY[cls.phase] = cls

    @abstractmethod
    def phase_instruction(self) -> str: ...

    @abstractmethod
    def voice(self) -> str: ...

    def __init__(self, chat_ctx: ChatContext | None = None) -> None:
        tts = cartesia.TTS(
            model="sonic-3",
            voice=self.voice(),
            speed=TTS_SPEED,
        )
        super().__init__(
            instructions=f"{BASE_INSTRUCTIONS}\n\n{self.phase_instruction()}",
            tools=[
                EndCallTool(),
                create_new_project,
                list_projects,
                set_active_project,
                get_project_context,
                get_blog_content,
                save_project_context,
                save_blog_content,
                research,
            ],
            chat_ctx=chat_ctx,
            tts=tts,
        )

    @abstractmethod
    async def on_enter(self) -> None: ...

    @function_tool()
    async def go_to_phase(
        self, context: RunContext, phase: int
    ) -> Agent | tuple[Agent, str | None] | str:
        """Switch to a different phase (1, 2, 3, or 4). Only call when the author asks to move to another phase—never call for the phase you are already in."""

        if phase not in (1, 2, 3, 4):
            return "Invalid phase. Please choose 1, 2, 3, or 4."
        if phase == self.phase:
            return f"Already in phase {phase}."

        next_class = self._REGISTRY.get(phase)
        if next_class is None:
            return "Invalid phase."

        transfer_msg = random.choice(TRANSFER_MESSAGES).format(name=next_class.name)
        handle = context.session.say(transfer_msg, allow_interruptions=False)
        await handle.wait_for_playout()

        next_agent = next_class(chat_ctx=context.session.history)
        return (next_agent, None)
