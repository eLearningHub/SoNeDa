conda-env:
	conda env create -f environment.yml

conda-env-remove:
	conda env remove --name sncli

requirements:
	pip install -r requirements.txt

poetry:
	wget https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py
	python install-poetry.py
	rm install-poetry.py