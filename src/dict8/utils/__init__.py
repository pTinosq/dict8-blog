import logging
from pathlib import Path

from dict8 import projects
from dict8.phases import PHASES

logger = logging.getLogger(__name__)


def load_prompt(name: str) -> str:
    path = Path(__file__).resolve().parent.parent / "prompts" / name
    return path.read_text()


def build_agent_enter_instructions(
    greeting: str,
    phases: tuple[int, ...] = (),
) -> str:
    """Build the on_enter instructions for an agent.

    Loads the optimised context files (``phase{N}ctx.md``) for each phase in
    *phases* from the active project directory and composes them into the
    greeting so the agent has full prior context.
    """
    if not phases:
        return greeting

    proj = projects.get_active_project()
    if proj is None:
        return greeting

    context_sections: list[str] = []
    for phase_num in phases:
        ctx_path = proj.root_dir / f"phase{phase_num}ctx.md"
        if not ctx_path.exists():
            continue
        content = ctx_path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        info = PHASES.get(phase_num)
        label = f"{info.name} (Phase {phase_num})" if info else f"Phase {phase_num}"
        context_sections.append(f"--- {label} context ---\n\n{content}")

    if not context_sections:
        return greeting

    preamble = (
        "The following context files summarise what was discussed in earlier "
        "phases. Use them to inform your conversation with the author. Do not "
        "recite them to the author; use them as background knowledge.\n\n"
    )
    joined = "\n\n".join(context_sections)
    return f"{preamble}{joined}\n\n---\n\n{greeting}"
