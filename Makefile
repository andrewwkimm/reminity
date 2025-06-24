help:
	cat Makefile

################################################################################

build:
	poetry install
	make reformat
	make lint
	make type_check
	make test

lint:
	poetry run ruff check --fix .

reformat:
	poetry run ruff format .

setup:
	pre-commit install --install-hooks
	poetry install

test:
	poetry run pytest -x --cov

type_check:
	poetry run mypy tests --ignore-missing-import

################################################################################

serve:
	poetry run python remivity/web/app.py

################################################################################

.PHONY: \
	build \
	help \
	lint \
	reformat \
	serve \
	setup \
	test \
	type_check
