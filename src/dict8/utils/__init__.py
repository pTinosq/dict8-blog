from pathlib import Path


def load_prompt(name: str) -> str:
    path = Path(__file__).resolve().parent.parent / "prompts" / name
    return path.read_text()


def build_agent_enter_instructions(
    greeting: str,
    phases: tuple[int, ...] = (),
    *,
    include_blog: bool = False,
    instruction: str = "Do not recite it to the author; use it as context.",
) -> str:
    """Return the greeting for an agent's on_enter. Phase/blog context is no longer used; transcripts are the record."""
    return greeting
