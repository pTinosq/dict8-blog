UV_VERSION=0.10.2

venv:
	uv venv

install-uv:
	curl --proto '=https' --tlsv1.2 -LsSf https://github.com/astral-sh/uv/releases/download/$(UV_VERSION)/uv-installer.sh | sh

install:
	uv sync

download-files:
	uv run --env-file=.env python -m dict8.main download-files

lint:
	uv run ruff check --fix
	uv run ruff format
	uv run pyright

dev-agent:
	uv run --env-file=.env python -m dict8.main dev

dev-agent-console:
	uv run --env-file=.env python -m dict8.main console

dev-worker:
	uv run --env-file=.env python -m dict8.worker