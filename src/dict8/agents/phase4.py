import logging

from livekit.agents import RunContext, function_tool

from dict8 import projects
from dict8.agents.base import BasePhaseAgent
from dict8.projects import ProjectStatus

logger = logging.getLogger(__name__)


class Phase4Agent(BasePhaseAgent):
    phase = 4

    @function_tool()
    async def finalize_blog(self, context: RunContext) -> str:
        """Finalize the session. Call this when the author is happy and ready to wrap up. This saves the final context and queues the blog for writing. After calling this, end the call."""

        # Optimise Phase 4 transcript.
        await self._run_context_optimization()

        # Mark the project as ready for the blog writer worker.
        proj = projects.get_active_project()
        if proj is None:
            return "Error: No active project."

        projects.set_project_status(proj.id, ProjectStatus.READY_FOR_WRITING)
        logger.info("Project '%s' marked as ready for writing", proj.name)

        return (
            "Done. The blog has been queued for writing and will be prepared shortly. "
            "Let the author know their blog will be sent to them soon, then end the call."
        )
