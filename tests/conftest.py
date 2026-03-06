import os

from dotenv import load_dotenv

load_dotenv()
# Allow importing dict8 (e.g. research_agent) during collection when .env has no API key.
os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-for-collection")
