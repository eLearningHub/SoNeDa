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

mypy-3.8:
	nox -s mypy-3.8

tests-3.8:
	nox -s tests-3.8

xdoctest-3.8:
	nox -s xdoctest-3.8

typeguard:
	nox -s typeguard
