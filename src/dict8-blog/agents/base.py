from abc import ABC, abstractmethod

from livekit.agents import Agent, RunContext, function_tool
from livekit.agents.beta.tools.end_call import EndCallTool
from livekit.agents.llm import ChatContext

BASE_INSTRUCTIONS = """You are a helpful voice AI assistant.
Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
You are curious, friendly, and have a sense of humor.

You operate in a phase system (phases 1-4). When the user asks to go to a different phase, call go_to_phase right away. Do not say anything first—the tool will play a short transfer message in your voice, then hand off to the new phase. Only call go_to_phase when switching to a phase you are not already in.

After a handoff you have the full conversation history; use it. If the user shared their name or other details earlier, remember and use them."""


class BasePhaseAgent(ABC, Agent):
    phase: int
    _REGISTRY: dict[int, type["BasePhaseAgent"]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "phase"):
            BasePhaseAgent._REGISTRY[cls.phase] = cls

    @abstractmethod
    def phase_instruction(self) -> str: ...

    @abstractmethod
    def voice(self) -> str: ...

    def __init__(self, chat_ctx: ChatContext | None = None) -> None:
        super().__init__(
            instructions=f"{BASE_INSTRUCTIONS}\n\n{self.phase_instruction()}",
            tools=[EndCallTool()],
            chat_ctx=chat_ctx,
            tts=self.voice(),
        )

    @abstractmethod
    async def on_enter(self) -> None: ...

    @function_tool()
    async def go_to_phase(
        self, context: RunContext, phase: int
    ) -> Agent | tuple[Agent, str | None] | str:
        """Switch to a different phase (1, 2, 3, or 4). Only call when the user asks to move to another phase—never call for the phase you are already in."""

        if phase not in (1, 2, 3, 4):
            return "Invalid phase. Please choose 1, 2, 3, or 4."
        if phase == self.phase:
            return f"Already in phase {phase}."

        transfer_msg = f"Transferring you now."
        handle = context.session.say(transfer_msg, allow_interruptions=False)
        await handle.wait_for_playout()

        next_class = self._REGISTRY.get(phase)
        if next_class is None:
            return "Invalid phase."

        next_agent = next_class(chat_ctx=context.session.history)
        return (next_agent, None)
