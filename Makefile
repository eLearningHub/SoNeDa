conda-env:
	conda env create -f environment.yml

conda-env-remove:
	conda env remove --name SoNeDa

pyenv:
	pyenv virtualenv 3.8.15 SoNeDa

requirements:
	pip install -r requirements.txt

install-poetry:
	wget https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py
	python install-poetry.py
	rm install-poetry.py

install:
	poetry install

run:
	poetry run soneda twitter --help