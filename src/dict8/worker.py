"""
Blog writer worker — a standalone process that polls the project store for
projects marked ``ready_for_writing``, runs the blog writer, and saves the
output.

Run separately from the LiveKit voice agent::

    python -m dict8.worker

No LiveKit dependency — just the OpenAI SDK and the project store.
"""

from __future__ import annotations

import asyncio
import logging

from dict8.llm.blog_writer import write_blog
from dict8.phases import ALL_PHASE_NUMBERS
from dict8.projects import ProjectStatus, default_store

logger = logging.getLogger(__name__)

POLL_INTERVAL_S = 10


async def process_project(project_id: str) -> bool:
    """Process a single project: read ctx files, write blog, update status.

    Returns True on success, False on failure.
    """
    proj = default_store.get_project(project_id)
    if proj is None:
        logger.error("Project %s not found — skipping", project_id)
        return False

    logger.info("Writing blog for project '%s' (%s)", proj.name, proj.id)
    default_store.set_project_status(proj.id, ProjectStatus.WRITING)

    ctx_files: dict[int, str] = {}
    for phase in ALL_PHASE_NUMBERS:
        ctx_path = proj.root_dir / f"phase{phase}ctx.md"
        if ctx_path.exists():
            ctx_files[phase] = ctx_path.read_text(encoding="utf-8")

    if not ctx_files:
        logger.error("No context files found for project '%s' — skipping", proj.name)
        default_store.set_project_status(proj.id, ProjectStatus.READY_FOR_WRITING)
        return False

    blog_md = await write_blog(ctx_files)
    if blog_md.startswith("Error:"):
        logger.error("Blog writing failed for '%s': %s", proj.name, blog_md)
        default_store.set_project_status(proj.id, ProjectStatus.READY_FOR_WRITING)
        return False

    blog_path = proj.root_dir / "blog.md"
    blog_path.write_text(blog_md, encoding="utf-8")
    default_store.set_project_status(proj.id, ProjectStatus.COMPLETE)
    logger.info("Blog saved: %s — status set to complete", blog_path)
    return True


async def process_queue() -> int:
    """Process all projects that are ready for writing.

    Returns the number of projects successfully processed.
    """
    ready = default_store.list_projects_by_status(ProjectStatus.READY_FOR_WRITING)
    if not ready:
        return 0

    logger.info("Found %d project(s) ready for writing", len(ready))
    count = 0
    for proj_info in ready:
        ok = await process_project(proj_info.id)
        if ok:
            count += 1
    return count


async def poll_loop() -> None:
    """Continuously poll for ready projects."""
    logger.info("Polling every %ds for projects ready to write...", POLL_INTERVAL_S)
    while True:
        try:
            processed = await process_queue()
            if processed:
                logger.info("Processed %d project(s) this cycle", processed)
        except Exception:
            logger.exception("Error during poll cycle")
        await asyncio.sleep(POLL_INTERVAL_S)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    asyncio.run(poll_loop())
