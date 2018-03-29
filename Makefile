clean:
	rm -rf build dist eljef_core.egg-info eljef/__pycache__ eljef/core/__pycache__

install:
	python3 setup.py install

lint:
	@tools/dolint.sh || true
