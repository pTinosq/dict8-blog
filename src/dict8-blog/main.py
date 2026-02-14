import logging
import os

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from .agents import ContextGatheringAgent


server = AgentServer()


@server.rtc_session(agent_name="dict8-blog-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="deepgram/nova-3:multi",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
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


if __name__ == "__main__":
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    agents.cli.run_app(server)
