import logging
from pathlib import Path
import asyncio

from dict8.llm.style_profiler import run_style_profiler

logger = logging.getLogger(__name__)

STYLE_PROFILES_DIR = Path(__file__).resolve().parent / "style_profiles"
ALLOWED_FILE_EXTENSIONS = [".md", ".html", ".txt"]


def generate_corpus(author_dir: Path) -> list[str]:
    """Generate a corpus of markdown files for an author"""
    corpus = []
    # First append the author.md file
    author_md_path = author_dir / "author.md"
    if author_md_path.exists():
        corpus.append(author_md_path.read_text())

    for file in author_dir.glob(f"*{ALLOWED_FILE_EXTENSIONS}"):
        if file.name == "author.md" or file.name == "style.md":
            continue

        corpus.append(file.read_text())
    return corpus


async def main():
    """Script to build a style profile for each author in the style_profiles directory"""

    # 1. Generate the corpus for each author
    for author_dir in STYLE_PROFILES_DIR.iterdir():
        if author_dir.is_dir():
            author_name = author_dir.name
            corpus = generate_corpus(author_dir)
            logger.info(f"Generated corpus of {len(corpus)} files for {author_name}")

            # Run style profiler for each author
            output = await run_style_profiler(corpus)
            manifest = output.manifest
            style_markdown = output.style_markdown

            logger.info(f"Generated style profile for {author_name}")
            break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
