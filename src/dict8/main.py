import logging
import os
import shutil
import tempfile
from pathlib import Path

from livekit import agents, rtc
from livekit.agents import (
    AgentServer,
    AgentSession,
    AudioConfig,
    BackgroundAudioPlayer,
    BuiltinAudioClip,
    room_io,
)
from livekit.plugins import cartesia, deepgram, noise_cancellation, openai, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from dict8.agents import Phase1Agent
from dict8.agents.base import BasePhaseAgent, TTS_SPEED
from dict8.projects import clear_active_project


# Raise memory warning threshold (default 500 MB is low for STT/LLM/TTS + research).
# Silero VAD "inference is slower than realtime" is demoted so it doesn't flood logs.
server = AgentServer(job_memory_warn_mb=2000)


@server.rtc_session(agent_name="dict8-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        llm=openai.LLM(model="gpt-5-nano"),
        stt=deepgram.STT(model="nova-3", language="multi"),
        tts=cartesia.TTS(
            model="sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
            speed=TTS_SPEED,
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    transcript_dir = Path(tempfile.mkdtemp(prefix="dict8-transcript-"))

    @session.on("conversation_item_added")
    def on_conversation_item(ev):
        """Append every conversation turn to the current phase's transcript."""
        try:
            agent = session.current_agent
            if not isinstance(agent, BasePhaseAgent):
                return
            if ev.item.role == "system":
                return
            text = (ev.item.text_content or "").strip()
            if not text:
                return
            prefix = "Agent: " if ev.item.role == "assistant" else "Human: "
            line = prefix + text + "\n"
            path = transcript_dir / f"phase{agent.phase}.md"
            with open(path, "a", encoding="utf-8") as f:
                f.write(line)
        except (RuntimeError, OSError):
            pass

    @session.on("close")
    def on_close(_ev):
        clear_active_project()
        try:
            shutil.rmtree(str(transcript_dir), ignore_errors=True)
        except OSError:
            pass

    await session.start(
        room=ctx.room,
        agent=Phase1Agent(transcript_dir=transcript_dir),
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
            AudioConfig(BuiltinAudioClip.HOLD_MUSIC, volume=0.6),
        ],
        ambient_sound=[
            AudioConfig(BuiltinAudioClip.OFFICE_AMBIENCE, volume=0.9),
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
