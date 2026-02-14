from dict8.agents.base import BasePhaseAgent
from dict8.utils import load_prompt

GREETING = load_prompt("context_gathering_agent_greeting.md")
BASE_PROMPT = load_prompt("context_gathering_agent_base.md")


class ContextGatheringAgent(BasePhaseAgent):
    phase = 1
    name = "research assistant"

    def phase_instruction(self) -> str:
        return BASE_PROMPT

    def voice(self) -> str:
        return "5ee9feff-1265-424a-9d7f-8e4d431a12c7"

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=GREETING)
