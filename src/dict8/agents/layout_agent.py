from dict8.agents.base import BasePhaseAgent
from dict8.utils import build_agent_enter_instructions, load_prompt

GREETING = load_prompt("layout_agent_greeting.md")
BASE_PROMPT = load_prompt("layout_agent_base.md")


class LayoutAgent(BasePhaseAgent):
    phase = 2
    name = "content editor"

    def phase_instruction(self) -> str:
        return BASE_PROMPT

    def voice(self) -> str:
        return "e8e5fffb-252c-436d-b842-8879b84445b6"

    async def on_enter(self) -> None:
        instructions = build_agent_enter_instructions(
            GREETING,
            (1,),
            include_blog=False,
            instruction="Do not recite it to the author; use it to agree on structure.",
        )
        await self.session.generate_reply(instructions=instructions)
