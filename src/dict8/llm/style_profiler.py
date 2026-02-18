import logging
from typing import Literal

from openai.types.shared_params import ChatModel

from dict8.llm.client import get_openai_client
from dict8.phases import PHASES
from dict8.utils import load_prompt
from pydantic import BaseModel

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

def run_style_profiler(corpus: list[str]) -> AuthorManifest: