conda-env:
	conda env create -f environment.yml

conda-env-remove:
	conda env remove --name SoNeDa

pyenv:
	pyenv virtualenv 3.8.15 SoNeDa

requirements:
	pip install -r requirements.txt

install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

install:
	poetry install

run:
	poetry run soneda twitter --help

pre-commit:
	nox -s pre-commit
