from dict8.agents.base import BasePhaseAgent
from dict8.utils import load_prompt

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
        await self.session.generate_reply(instructions=GREETING)
