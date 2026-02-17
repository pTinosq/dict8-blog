from dataclasses import dataclass


@dataclass(frozen=True)
class PhaseInfo:
    number: int
    name: str  # "Context Gathering", "Layout", etc.
    agent_name: str  # how the agent introduces itself during transfers
    voice_id: str  # Cartesia voice ID
    prior_phases: tuple[int, ...]  # which phase ctx files to load on enter


PHASES: dict[int, PhaseInfo] = {
    1: PhaseInfo(
        number=1,
        name="Context Gathering",
        agent_name="research assistant",
        voice_id="5ee9feff-1265-424a-9d7f-8e4d431a12c7",
        prior_phases=(),
    ),
    2: PhaseInfo(
        number=2,
        name="Layout",
        agent_name="content editor",
        voice_id="e8e5fffb-252c-436d-b842-8879b84445b6",
        prior_phases=(1,),
    ),
    3: PhaseInfo(
        number=3,
        name="Writing",
        agent_name="writer",
        voice_id="2f251ac3-89a9-4a77-a452-704b474ccd01",
        prior_phases=(1, 2),
    ),
    4: PhaseInfo(
        number=4,
        name="Overview",
        agent_name="overview",
        voice_id="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        prior_phases=(1, 2, 3),
    ),
}

ALL_PHASE_NUMBERS = tuple(PHASES.keys())
