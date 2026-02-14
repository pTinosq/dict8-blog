from .base import BasePhaseAgent

_VOICE = "cartesia/sonic-3:5ee9feff-1265-424a-9d7f-8e4d431a12c7"

_PHASE_INSTRUCTION = """Phase 1: Focus on discovery and understanding.
Ask open questions, listen, and summarize what the user shares.
Do not jump to solutions or options—first understand the situation and what matters to the user."""

_GREETING = "Greet the user warmly and offer your assistance. Say you are here for discovery and understanding. Keep it brief and inviting."


class ContextGatheringAgent(BasePhaseAgent):
    phase = 1

    def phase_instruction(self) -> str:
        return _PHASE_INSTRUCTION

    def voice(self) -> str:
        return _VOICE

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=_GREETING)
