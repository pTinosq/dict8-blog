"""Test that after the welcome, choosing an existing project leads to list_projects and set_active_project."""

import tempfile
from pathlib import Path

import pytest

from livekit.agents import AgentSession
from livekit.plugins import openai

from dict8 import projects
from dict8.agent import SESSION_LLM_MODEL, create_initial_agent
from tests.utils import requires_openai_key


def _has_function_call(result, name: str) -> bool:
    """True if this run result contains a function call with the given name."""
    try:
        result.expect.contains_function_call(name=name)
        return True
    except AssertionError:
        return False


@requires_openai_key
@pytest.mark.asyncio
async def test_after_welcome_work_on_existing_project_calls_list_projects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When the user chooses an existing project and then identifies it, the agent
    calls list_projects and set_active_project at some point in the conversation."""
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

        res1 = await session.run(user_input="I'd like to work on an existing blog.")
        res2 = await session.run(user_input="Yes, that one.")

    # Assert over the whole conversation: both tools must appear in some turn
    list_in_res1 = _has_function_call(res1, "list_projects")
    list_in_res2 = _has_function_call(res2, "list_projects")
    set_in_res1 = _has_function_call(res1, "set_active_project")
    set_in_res2 = _has_function_call(res2, "set_active_project")

    assert list_in_res1 or list_in_res2, "list_projects should be called in turn 1 or 2"
    assert (
        set_in_res1 or set_in_res2
    ), "set_active_project should be called in turn 1 or 2"
