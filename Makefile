.PHONY: all fix lint ssort isort black pyright flake8 test

all: fix lint test run

fix: ssort isort black

lint: pyright flake8

test:
	poetry run python -m pytest --cov=auto_docstring .

run:
	poetry run python -m auto_docstring

ssort:
	poetry run python -m ssort .

isort:
	poetry run python -m isort --profile black .

black:
	poetry run python -m black .

pyright:
	poetry run python -m pyright .

flake8:
	poetry run python -m flake8 .
