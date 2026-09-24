MAIN = a_maze_ing.py
CONFIG = config.txt


install:
	# install project dependencies using pip, uv, pipx...

run:
	python3 $(MAIN) $(CONFIG)

debug:
	python -m pdb $(MAIN) $(CONFIG)

clean:
	rm -R __pycache__ .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict
