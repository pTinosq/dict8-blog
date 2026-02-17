import logging
import random
from abc import ABC
from pathlib import Path

from livekit.agents import Agent, RunContext, function_tool
from livekit.agents.beta.tools.end_call import EndCallTool
from livekit.agents.llm import ChatContext
from livekit.plugins import cartesia

from dict8 import projects
from dict8.llm.context_optimizer import optimize_context
from dict8.agents.research_agent import run_research
from dict8.phases import PHASES
from dict8.utils import build_agent_enter_instructions, load_prompt

logger = logging.getLogger(__name__)

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
    """Set the active project by id. Transcripts are stored under this project. Do not announce to the author."""
    try:
        projects.set_active_project(project_id)
        proj = projects.get_active_project()
        if proj is None:
            return "No active project. Use list_projects and set_active_project first."
        return f"Active project is now '{proj.name}' (id: {proj.id})."
    except ValueError as e:
        return str(e)


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
    """Base class for all phase agents.

    Subclasses only need to set ``phase = N`` as a class attribute.
    Everything else — voice, prompts, on_enter behaviour — is derived from
    the central ``PHASES`` config and can be overridden when needed.
    """

    phase: int
    _REGISTRY: dict[int, type["BasePhaseAgent"]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "phase"):
            BasePhaseAgent._REGISTRY[cls.phase] = cls

    def phase_instruction(self) -> str:
        return load_prompt(f"phase{self.phase}_base.md")

    def voice(self) -> str:
        return PHASES[self.phase].voice_id

    async def on_enter(self) -> None:
        info = PHASES[self.phase]
        greeting = load_prompt(f"phase{self.phase}_greeting.md")
        instructions = build_agent_enter_instructions(greeting, info.prior_phases)
        await self.session.generate_reply(instructions=instructions)

    # ------------------------------------------------------------------

    def __init__(
        self,
        transcript_dir: Path,
        chat_ctx: ChatContext | None = None,
    ) -> None:
        self.transcript_dir = transcript_dir
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
                research,
            ],
            chat_ctx=chat_ctx,
            tts=tts,
        )

    async def _run_context_optimization(self) -> None:
        """Read this phase's transcript and produce an optimised context file."""
        transcript_path = self.transcript_dir / f"phase{self.phase}.md"
        if not transcript_path.exists():
            logger.warning(
                "No transcript found at %s — skipping optimisation", transcript_path
            )
            return

        transcript = transcript_path.read_text(encoding="utf-8")
        if not transcript.strip():
            logger.warning(
                "Transcript at %s is empty — skipping optimisation", transcript_path
            )
            return

        proj = projects.get_active_project()
        if proj is None:
            logger.warning("No active project — cannot save context file")
            return

        result = await optimize_context(self.phase, transcript)
        if result.startswith("Error:"):
            logger.error(
                "Context optimisation failed for phase %d: %s", self.phase, result
            )
            return

        ctx_path = proj.root_dir / f"phase{self.phase}ctx.md"
        ctx_path.parent.mkdir(parents=True, exist_ok=True)
        ctx_path.write_text(result, encoding="utf-8")
        logger.info("Saved context file: %s", ctx_path)

    @function_tool()
    async def go_to_phase(
        self, context: RunContext, phase: int
    ) -> Agent | tuple[Agent, str | None] | str:
        """Switch to a different phase (1, 2, 3, or 4). Only call when the author asks to move to another phase—never call for the phase you are already in."""

        if phase not in PHASES:
            return f"Invalid phase. Please choose from: {', '.join(str(n) for n in PHASES)}."
        if phase == self.phase:
            return f"Already in phase {phase}."

        next_class = self._REGISTRY.get(phase)
        if next_class is None:
            return "Invalid phase."

        # Guard: a project must exist before we can save context or move on.
        if projects.get_active_project() is None:
            return "Error: No active project. You must call create_new_project first before switching phases."

        # Optimise the current phase's transcript before handing off.
        await self._run_context_optimization()

        agent_name = PHASES[phase].agent_name
        transfer_msg = random.choice(TRANSFER_MESSAGES).format(name=agent_name)
        handle = context.session.say(transfer_msg, allow_interruptions=False)
        await handle.wait_for_playout()

        next_agent = next_class(
            transcript_dir=self.transcript_dir,
            chat_ctx=context.session.history,
        )
        return (next_agent, None)
