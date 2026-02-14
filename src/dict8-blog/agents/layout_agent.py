from .base import BasePhaseAgent

_VOICE = "cartesia/sonic-3:e8e5fffb-252c-436d-b842-8879b84445b6"

_PHASE_INSTRUCTION = """Phase 2: you're judt a really funny guy, you just find everything so joyful and whimsical.."""

_GREETING = "Say one short line only: you are in phase 2 (options and choices). Ask what they would like to explore or decide. Keep it brief."


class LayoutAgent(BasePhaseAgent):
    phase = 2

    def phase_instruction(self) -> str:
        return _PHASE_INSTRUCTION

    def voice(self) -> str:
        return _VOICE

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=_GREETING)
