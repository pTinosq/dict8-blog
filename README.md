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
