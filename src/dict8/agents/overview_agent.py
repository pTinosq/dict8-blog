from dict8.agents.base import BasePhaseAgent
from dict8.utils import load_prompt

GREETING = load_prompt("overview_agent_greeting.md")
BASE_PROMPT = load_prompt("overview_agent_base.md")


class OverviewAgent(BasePhaseAgent):
    phase = 4
    name = "overview"

    def phase_instruction(self) -> str:
        return BASE_PROMPT

    def voice(self) -> str:
        return "9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=GREETING)
