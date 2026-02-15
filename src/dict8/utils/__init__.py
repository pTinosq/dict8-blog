from pathlib import Path

from dict8 import projects


def load_prompt(name: str) -> str:
    path = Path(__file__).resolve().parent.parent / "prompts" / name
    return path.read_text()


def build_agent_enter_instructions(
    greeting: str,
    phases: tuple[int, ...],
    *,
    include_blog: bool = False,
    instruction: str = "Do not recite it to the author; use it as context.",
) -> str:
    """Build the full instruction string for an agent's on_enter: greeting plus context from earlier phases and optionally the blog. When there is no context, returns just the greeting."""
    proj = projects.get_active_project()
    if not proj:
        return greeting
    parts = []
    for phase in phases:
        ctx = proj.get_context_for_phase(phase)
        if ctx:
            parts.append(f"--- Phase {phase} context ---\n{ctx}")
    if include_blog:
        blog = proj.get_blog()
        if blog:
            parts.append(f"--- Current blog ---\n{blog}")
    if not parts:
        return greeting
    context = f"Use the following context. {instruction}\n\n" + "\n\n".join(parts)
    return f"{greeting}\n\n{context}"
