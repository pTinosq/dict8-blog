import logging
from typing import Literal

from openai.types.responses.response_input_param import ResponseInputParam
from openai.types.responses.response_input_item_param import ResponseInputItemParam
from openai.types.shared_params import ChatModel

from dict8.llm.client import get_openai_client
from dict8.utils import load_prompt
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


BASE_INSTRUCTIONS = load_prompt("style_profiler.md")

MODEL: ChatModel = "gpt-5-nano"


class StyleAxes(BaseModel):
    analytical: float  # 0-1
    emotional: float
    playful: float
    technical: float
    persuasive: float


class AuthorManifest(BaseModel):
    style_id: str
    display_name: str
    summary: str

    tone_tags: list[str]
    audience_tags: list[str]

    energy_level: Literal["low", "medium", "high"]
    emotional_temperature: Literal["cool", "warm", "intense"]
    confidence_level: Literal["measured", "assertive", "provocative"]

    formality_level: Literal["low", "medium", "high"]
    lexical_complexity: Literal["simple", "moderate", "advanced"]
    conceptual_abstraction: Literal["concrete", "mixed", "abstract"]

    paragraph_density: Literal["sparse", "moderate", "dense"]
    sentence_style: Literal["short", "mixed", "long", "high_variance"]

    narrative_voice: Literal["first_person", "impersonal", "mixed"]
    direct_address_frequency: Literal["none", "light", "frequent"]
    rhetorical_question_usage: Literal["none", "light", "frequent"]

    opening_style: str
    argument_structure: str

    axes: StyleAxes


class StyleProfileOutput(BaseModel):
    manifest: AuthorManifest
    style_markdown: str


async def run_style_profiler(corpus: list[str]) -> StyleProfileOutput:
    """
    Runs the Style Distillation Pipeline for a single author.

    Args:
        corpus: List of raw markdown / html strings for a single author,
                including author.md as the first element if available.

    Returns:
        StyleProfileOutput (validated via Pydantic structured output)
    """

    if not corpus:
        raise ValueError("Corpus is empty. Cannot run style profiler.")

    client = get_openai_client()

    # Combine corpus into a single analysis payload
    # You may want to truncate or chunk upstream if extremely large.
    joined_corpus = "\n\n--- DOCUMENT BREAK ---\n\n".join(corpus)

    system_msg: ResponseInputItemParam = {
        "role": "system",
        "content": BASE_INSTRUCTIONS,
    }
    user_msg: ResponseInputItemParam = {
        "role": "user",
        "content": f"# Corpus\n\n{joined_corpus}",
    }
    messages: ResponseInputParam = [system_msg, user_msg]

    try:
        response = await client.responses.parse(
            model=MODEL,
            input=messages,
            text_format=StyleProfileOutput,
        )

        output = response.output_parsed
        if output is None:
            raise ValueError(
                "Model returned no parsed output (possible refusal or empty response)."
            )

        manifest = output.manifest
        style_markdown = output.style_markdown

        logger.info(
            "Style profiling complete",
        )

        return StyleProfileOutput(
            manifest=manifest,
            style_markdown=style_markdown,
        )

    except ValidationError as e:
        logger.exception("Structured output validation failed.", exc_info=e)
        raise

    except Exception as e:
        logger.exception("Style profiling failed.", exc_info=e)
        raise
