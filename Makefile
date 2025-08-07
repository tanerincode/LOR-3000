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

docker-build:
	docker build -t lor3000:latest .

docker-run:
	docker run --rm -p 8000:8000 \
	  -e OPENAI_API_KEY=$${OPENAI_API_KEY} \
	  -e APP_CONFIG_FILE=/config/app.yaml \
	  -v $${PWD}/config:/config \
	  lor3000:latest
