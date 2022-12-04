install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

install:
	poetry install

run:
	poetry run soneda twitter --help

pre-commit:
	nox -s pre-commit

safety:
	nox -s safety
