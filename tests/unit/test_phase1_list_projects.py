"""Test that after the welcome, asking to work on an existing project triggers list_projects."""

import tempfile
from pathlib import Path

import pytest

from livekit.agents import AgentSession
from livekit.plugins import openai

from dict8 import projects
from dict8.agent import SESSION_LLM_MODEL, create_initial_agent
from tests.utils import requires_openai_key


@requires_openai_key
@pytest.mark.asyncio
async def test_after_welcome_work_on_existing_project_calls_list_projects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When the user says they want to work on an existing project, the agent calls list_projects,
    then after they identify it by topic the agent calls set_active_project."""
    transcript_dir = Path(tempfile.mkdtemp(prefix="dict8-test-"))
    project_root = Path(tempfile.mkdtemp(prefix="dict8-projects-"))
    store = projects.ProjectStore(root=project_root)
    store.create_project(
        slug="cyclical-design-trends",
        name="Cyclical design trends",
        description="The blog is about cyclical design trends",
    )
    monkeypatch.setattr(projects, "default_store", store)

    llm = openai.LLM(model=SESSION_LLM_MODEL)
    agent = create_initial_agent(transcript_dir, resume_phase=1)

    async with AgentSession(llm=llm) as session:
        await session.start(agent)

        # Turn 1: user wants to work on an existing project -> agent must call list_projects
        res1 = await session.run(user_input="I'd like to work on an existing blog.")
        res1.expect.contains_function_call(name="list_projects")

        # Turn 2: user confirms which project -> agent must call set_active_project (or may have already in turn 1 when only one project)
        res2 = await session.run(user_input="Yes, that one.")
        try:
            res1.expect.contains_function_call(name="set_active_project")
        except AssertionError:
            res2.expect.contains_function_call(name="set_active_project")
