BINDIR = $(if $(wildcard venv/bin), venv/bin/, '')


setup::
	python -m venv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install -e .


clean::
	rm -rf dist build

clean-full:: clean
	rm -rf venv
	find src -depth -name __pycache__ -type d -exec rm -rf "{}" \;


lint::
	${BINDIR}tidypy check


build:: clean
	${BINDIR}python setup.py sdist
	${BINDIR}python setup.py bdist_wheel

publish::
	${BINDIR}twine upload dist/*

