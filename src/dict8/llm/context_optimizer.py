import logging

from openai.types.shared_params import ChatModel

from dict8.llm.client import get_openai_client
from dict8.utils import load_prompt

logger = logging.getLogger(__name__)

NOTES_INSTRUCTIONS = load_prompt("notes_optimizer.md")
STRUCTURE_INSTRUCTIONS = load_prompt("structure_optimizer.md")

MODEL: ChatModel = "gpt-5-nano"


async def optimize_artifact(artifact: str, transcript: str) -> str:
    """Convert a transcript into an optimized v1 artifact markdown file.

    Returns the optimized markdown string, or an error string starting with
    ``Error:``.
    """
    if artifact == "notes":
        system_prompt = NOTES_INSTRUCTIONS
    elif artifact == "structure":
        system_prompt = STRUCTURE_INSTRUCTIONS
    else:
        return f"Error: Unknown artifact '{artifact}'."

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
