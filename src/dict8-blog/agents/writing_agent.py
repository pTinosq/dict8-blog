from .base import BasePhaseAgent

_VOICE = "cartesia/sonic-3:2f251ac3-89a9-4a77-a452-704b474ccd01"

_PHASE_INSTRUCTION = """Phase 3: You are a depressed sad and not intereseted person."""

_GREETING = "Say one short line only: you are in phase 3 (planning). Ask what they want to plan or what the next steps are. Keep it brief."


class WritingAgent(BasePhaseAgent):
    phase = 3

    def phase_instruction(self) -> str:
        return _PHASE_INSTRUCTION

    def voice(self) -> str:
        return _VOICE

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=_GREETING)
