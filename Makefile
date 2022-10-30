conda-env:
	conda env create -f environment.yml

conda-env-remove:
	conda env remove --name sncli

requirements:
	pip install -r requirements.txt
