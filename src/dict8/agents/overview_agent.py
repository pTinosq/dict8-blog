from dict8.agents.base import BasePhaseAgent
from dict8.utils import build_agent_enter_instructions, load_prompt

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
        instructions = build_agent_enter_instructions(
            GREETING,
            (1, 2, 3),
            include_blog=True,
            instruction="Do not recite it to the author; use it to run the overview.",
        )
        await self.session.generate_reply(instructions=instructions)
