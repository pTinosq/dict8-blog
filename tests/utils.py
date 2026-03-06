import functools
import os

import pytest


def requires_openai_key(func):
    """Skip the test if OPENAI_API_KEY from .env is missing or the collection dummy."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key or api_key.startswith("sk-dummy"):
            pytest.skip(
                "OPENAI_API_KEY from .env required (uses LiveKit agent session)."
            )
        return await func(*args, **kwargs)

    return wrapper
