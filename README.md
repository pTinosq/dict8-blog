# Dict8 blog

Voice agent to build blogs.

## SIP setup

I recommend following the Twilio SIP setup guide [here](https://docs.livekit.io/telephony/start/providers/twilio/).

1. Buy a phone number from Twilio
2. Set up your SIP trunk
3. Add your phone number to the SIP trunk
4. Set up LiveKit dashboard (Dispatch, trunks, etc.)

The agent uses **explicit dispatch** with `agent_name="my-telephony-agent"`. For inbound calls, create a dispatch rule that routes to this agent (e.g. with `lk sip dispatch create dispatch-rule.json`). See [Agents telephony integration](https://docs.livekit.io/telephony/agents).

## Local setup

1. Run `make install-uv` (Install UV)
2. Run `make venv` (Set up venv)
3. Run `make install` (Install dependencies)
4. Run `make download-files` (Download model files)
5. Run `make dev` (Run the application - normal mode)
6. Run `make dev-console` (Run the application - console mode)

## Why use BYOK?

All LLM, STT, and TTS calls use your own API keys rather than routing through LiveKit's inference gateway. This is considerably cheaper and avoids hitting LiveKit's built-in credit quotas ($2.50 on the Build plan).

You'll need keys for:

- **OpenAI** — LLM (chat completions, context optimisation, blog writing)
- **Deepgram** — STT (speech-to-text). Deepgram gives you $200 of free credit, which is roughly 7 days of continuous phone call time.
- **Cartesia** — TTS (text-to-speech)

Set these up in your `.env` file (see `.env.example`).
