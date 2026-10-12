MAIN = a_maze_ing.py
CONFIG = config.txt
PYTHON = python3
MIN_PYTHON = 3.11.15

#python3 -m venv .venv
#. .venv/bin/activate
#python -m pip install build
#make install-dev
#python a_maze_ing.py
#make build

install:
	@$(PYTHON) --version
	@echo "Required $(PYTHON) >= $(MIN_PYTHON)"
	@echo "No external dependency needed"
	@python -m pip --version
	@python -m pip install . # install from pyproject.toml

install-dev: # per lavorare sul codice senza reinstallarlo continuamente
	@$(PYTHON) --version
	@$(PYTHON) -m pip --version
	@$(PYTHON) -m pip install -e .

build:
	@$(PYTHON) -m build --wheel --sdist --outdir .

run:
	$(PYTHON) $(MAIN) $(CONFIG)

runcarli:
	python3.12 $(MAIN) $(CONFIG)

debug:
	python -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +
	rm maze.txt
	rm -rf build dist src/*.egg-info
	rm -f mazegen-*.whl mazegen-*.tar.gz
	@rm -rf .ruff_cache

lint:
	@clear
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

auto-lint:
	ruff format .
	black .

.PHONY: install install-dev build run debug clean lint lint-strict auto-lint
