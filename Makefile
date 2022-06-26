.PHONY: all fix lint ssort isort black pyright flake8 test

all: fix lint test run

fix: ssort isort black

lint: pyright flake8

test:
	poetry run python -m pytest --cov=auto_docstring -vv auto_docstring

run:
	poetry run python -m auto_docstring test.py

ssort:
	poetry run python -m ssort auto_docstring

isort:
	poetry run python -m isort --profile black auto_docstring

black:
	poetry run python -m black auto_docstring

pyright:
	poetry run python -m pyright auto_docstring

flake8:
	poetry run python -m flake8 auto_docstring
