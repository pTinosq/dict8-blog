from functools import lru_cache

from openai import AsyncOpenAI


@lru_cache(maxsize=1)
def get_openai_client() -> AsyncOpenAI:
    return AsyncOpenAI()
