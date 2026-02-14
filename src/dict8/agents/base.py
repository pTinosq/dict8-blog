import random
from abc import ABC, abstractmethod

from livekit.agents import Agent, RunContext, function_tool
from livekit.agents.beta.tools.end_call import EndCallTool
from livekit.agents.llm import ChatContext
from livekit.plugins import cartesia
from dict8.utils import load_prompt

BASE_INSTRUCTIONS = load_prompt("sys.md")

# Cartesia TTS speech speed (0.6–2.0). Lower = slower, more natural for conversation.
TTS_SPEED = 0.93

TRANSFER_MESSAGES = [
    "Just a second please, I'm going to transfer you to our {name}.",
    "One moment, I'll send you over to our {name}.",
    "Hold on a sec, I'm connecting you with our {name}.",
    "Give me just a second. I'm transferring you to our {name}.",
]


class BasePhaseAgent(ABC, Agent):
    phase: int
    name: str
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
        tts = cartesia.TTS(
            model="sonic-3",
            voice=self.voice(),
            speed=TTS_SPEED,
        )
        super().__init__(
            instructions=f"{BASE_INSTRUCTIONS}\n\n{self.phase_instruction()}",
            tools=[EndCallTool()],
            chat_ctx=chat_ctx,
            tts=tts,
        )

    @abstractmethod
    async def on_enter(self) -> None: ...

    @function_tool()
    async def go_to_phase(
        self, context: RunContext, phase: int
    ) -> Agent | tuple[Agent, str | None] | str:
        """Switch to a different phase (1, 2, 3, or 4). Only call when the author asks to move to another phase—never call for the phase you are already in."""

        if phase not in (1, 2, 3, 4):
            return "Invalid phase. Please choose 1, 2, 3, or 4."
        if phase == self.phase:
            return f"Already in phase {phase}."

        next_class = self._REGISTRY.get(phase)
        if next_class is None:
            return "Invalid phase."

        transfer_msg = random.choice(TRANSFER_MESSAGES).format(name=next_class.name)
        handle = context.session.say(transfer_msg, allow_interruptions=False)
        await handle.wait_for_playout()

        next_agent = next_class(chat_ctx=context.session.history)
        return (next_agent, None)
