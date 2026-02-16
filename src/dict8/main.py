import logging
import os

from livekit import agents, rtc
from livekit.agents import (
    AgentServer,
    AgentSession,
    AudioConfig,
    BackgroundAudioPlayer,
    BuiltinAudioClip,
    room_io,
)
from livekit.plugins import cartesia, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from dict8.agents import ContextGatheringAgent
from dict8.agents.base import TTS_SPEED


# Raise memory warning threshold (default 500 MB is low for STT/LLM/TTS + research).
# Silero VAD "inference is slower than realtime" is demoted so it doesn't flood logs.
server = AgentServer(job_memory_warn_mb=2000)


@server.rtc_session(agent_name="dict8-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="deepgram/nova-3:multi",
        llm="openai/gpt-4.1-mini",
        tts=cartesia.TTS(
            model="sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
            speed=TTS_SPEED,
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=ContextGatheringAgent(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )

    # Thinking sound plays when agent state is "thinking" (e.g. during research tool).
    # Builtins match the official example; pipeline may not set thinking during tool execution.
    background_audio = BackgroundAudioPlayer(
        thinking_sound=[
            AudioConfig(BuiltinAudioClip.KEYBOARD_TYPING, volume=0.8),
            AudioConfig(BuiltinAudioClip.KEYBOARD_TYPING2, volume=0.7),
        ],
    )
    await background_audio.start(room=ctx.room, agent_session=session)


if __name__ == "__main__":
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Reduce Silero VAD "inference is slower than realtime" log noise (still logs errors).
    logging.getLogger("livekit.plugins.silero").setLevel(logging.ERROR)
    agents.cli.run_app(server)
