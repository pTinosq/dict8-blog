from dict8.agents.base import BasePhaseAgent
from dict8.utils import load_prompt

GREETING = load_prompt("writing_agent_greeting.md")
BASE_PROMPT = load_prompt("writing_agent_base.md")


class WritingAgent(BasePhaseAgent):
    phase = 3

    def phase_instruction(self) -> str:
        return BASE_PROMPT

    def voice(self) -> str:
        return "cartesia/sonic-3:2f251ac3-89a9-4a77-a452-704b474ccd01"

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=GREETING)
