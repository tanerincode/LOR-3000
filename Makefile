.PHONY: run install lint format test

install:
	python -m pip install -r requirements.txt

run:
	PYTHONPATH=src uvicorn main:app --reload

format:
	python -m black src tests || true

lint:
	python -m ruff check src tests || true

test:
	PYTHONPATH=src pytest -q || true

typecheck:
	PYTHONPATH=src mypy src

precommit-install:
	. .venv/bin/activate && pre-commit install

precommit-run:
	. .venv/bin/activate && pre-commit run --all-files
