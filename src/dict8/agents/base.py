import logging
import random
from pathlib import Path

from livekit.agents import Agent, RunContext, function_tool
from livekit.agents.beta.tools.end_call import EndCallTool
from livekit.agents.llm import ChatContext
from livekit.plugins import cartesia

from dict8 import projects
from dict8.agents.research_agent import run_research
from dict8.llm.context_optimizer import optimize_artifact
from dict8.utils import load_prompt

logger = logging.getLogger(__name__)

BASE_INSTRUCTIONS = load_prompt("sys.md")
GREETING = load_prompt("main_greeting.md")

# Cartesia TTS speech speed (0.6–2.0). Lower = slower, more natural for conversation.
TTS_SPEED = 0.93

RESEARCH_INTRO_PHRASES = [
    "I googled it and ",
    "I searched it up and ",
    "I looked it up and ",
    "I checked and ",
    "I ran a quick search and ",
]


@function_tool()
async def create_new_project(slug: str, name: str, description: str) -> str:
    """Create a brand-new blog project and make it active.

    Slug: URL-friendly (e.g. my-blog-topic). Name: display title. Description: brief, disambiguating summary for model context (e.g. 'Navy SEALs training' vs 'Pet seal care').
    Do not announce to the author.
    """
    try:
        proj = projects.create_project(slug, name, description)
        projects.set_active_project(proj.id)
        return f"Created and active. Id: {proj.id}"
    except ValueError as e:
        return str(e)


@function_tool()
async def list_projects() -> str:
    """List projects (id, name, slug, description). Use the list to match the author's words to one project and call set_active_project with its id. Do not announce tool names to the author."""
    items = projects.list_projects()
    if not items:
        return "No projects yet. Use create_new_project to create one."
    lines = [f"- {p.name} (id: {p.id}, slug: {p.slug}): {p.description}" for p in items]
    return "\n".join(lines)


@function_tool()
async def set_active_project(project_id: str) -> str:
    """Set the active project by id. Do not announce tool names or ids."""
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


class Dict8Agent(Agent):
    def __init__(
        self,
        transcript_dir: Path,
        chat_ctx: ChatContext | None = None,
    ) -> None:
        self.transcript_dir = transcript_dir
        tts = cartesia.TTS(
            model="sonic-3",
            voice="5ee9feff-1265-424a-9d7f-8e4d431a12c7",
            speed=TTS_SPEED,
        )
        super().__init__(
            instructions=BASE_INSTRUCTIONS,
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

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=GREETING)

    async def refresh_project_artifacts(self) -> None:
        """Generate v1 artifacts from the conversation transcript."""
        proj = projects.get_active_project()
        if proj is None:
            logger.warning("No active project — cannot save notes/structure files")
            return

        transcript_path = self.transcript_dir / "call.md"
        if not transcript_path.exists():
            logger.warning("No transcript file found — skipping refresh")
            return
        transcript = transcript_path.read_text(encoding="utf-8").strip()
        if not transcript:
            logger.warning("No transcript content available — skipping refresh")
            return

        notes = await optimize_artifact("notes", transcript)
        if notes.startswith("Error:"):
            logger.error("Notes generation failed: %s", notes)
        else:
            notes_path = proj.root_dir / "notes.md"
            notes_path.parent.mkdir(parents=True, exist_ok=True)
            notes_path.write_text(notes, encoding="utf-8")
            logger.info("Saved notes file: %s", notes_path)

        structure = await optimize_artifact("structure", transcript)
        if structure.startswith("Error:"):
            logger.error("Structure generation failed: %s", structure)
            return

        structure_path = proj.root_dir / "structure.md"
        structure_path.parent.mkdir(parents=True, exist_ok=True)
        structure_path.write_text(structure, encoding="utf-8")
        logger.info("Saved structure file: %s", structure_path)
