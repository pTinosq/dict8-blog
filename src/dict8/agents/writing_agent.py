from dict8.agents.base import BasePhaseAgent
from dict8.utils import build_agent_enter_instructions, load_prompt

GREETING = load_prompt("writing_agent_greeting.md")
BASE_PROMPT = load_prompt("writing_agent_base.md")


class WritingAgent(BasePhaseAgent):
    phase = 3
    name = "writer"

    def phase_instruction(self) -> str:
        return BASE_PROMPT

    def voice(self) -> str:
        return "2f251ac3-89a9-4a77-a452-704b474ccd01"

    async def on_enter(self) -> None:
        instructions = build_agent_enter_instructions(
            GREETING,
            (1, 2),
            include_blog=True,
            instruction="Do not recite it to the author; use it to write and revise sections.",
        )
        await self.session.generate_reply(instructions=instructions)
