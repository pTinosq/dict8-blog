import logging

from openai.types.shared_params import ChatModel

from dict8.llm.client import get_openai_client
from dict8.phases import PHASES
from dict8.utils import load_prompt

logger = logging.getLogger(__name__)


BASE_INSTRUCTIONS = load_prompt("context_optimizer.md")

MODEL: ChatModel = "gpt-5-nano"


async def optimize_context(phase: int, transcript: str) -> str:
    """Convert a raw phase transcript into an optimised context markdown file.

    Returns the optimised context string, or an error string starting with
    ``Error:``.
    """
    phase_name = PHASES[phase].name if phase in PHASES else f"Phase {phase}"
    system_prompt = BASE_INSTRUCTIONS.replace("{{PHASE}}", str(phase)).replace(
        "{{PHASE_NAME}}", phase_name
    )

    try:
        client = get_openai_client()

        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
        )
        text = (response.choices[0].message.content or "").strip()
        if not text:
            return "Error: Context optimizer returned empty output."
        return text
    except Exception as e:
        logger.exception("Context optimization failed")
        return f"Error: {type(e).__name__}: {e}"
