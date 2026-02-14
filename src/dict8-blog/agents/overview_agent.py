from .base import BasePhaseAgent

_VOICE = "cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"

_PHASE_INSTRUCTION = """Phase 4: You just get angry at everything. you're having a terrible day and are not interested in chatting at all.."""

_GREETING = "Say one short line only: you are in phase 4 (wrap-up). Ask if they want to summarize, confirm next steps, or schedule a follow-up. Keep it brief."


class OverviewAgent(BasePhaseAgent):
    phase = 4

    def phase_instruction(self) -> str:
        return _PHASE_INSTRUCTION

    def voice(self) -> str:
        return _VOICE

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=_GREETING)
