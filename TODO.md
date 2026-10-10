# Urgent
- print to file solving algorithm sequence and test the result with moulinette(implemneted must be tested with moulinette)
- Show/Hide a valid shortest path from the entrance to the exit. (just put a default flag parameter in print self hide=False that prints 3 spaces if True)

# To do at the end of the project:
- quando si modificano le dimensioni del terminale fai subito un reload del labirinto
- generic error handling in main
- remove import traceback
- linting
- Complete the readme

# MazeGenerator
You must provide a short documentation describing how to:
Instantiate and use your generator, with at least a basic example.
Pass custom parameters (e.g., size, seed).
Access the generated structure, and access at least a solution.
This entire reusable module (code and documentation) must be available in a single file
suitable for a later installation by pip.
This package must be called mazegen-* and the file must be located at the root of your
git repository.
Use whl extension (not tar.gz)
Example of a full filename: mazegen-1.0.0-py3-none-any.whl
You must provide in your Git repository all needed elements to build the package. This
will be asked during the evaluation: in a virtualenv or equivalent, install the needed tools
and build your package again from your sources.

# Bonus
A default (non-perfect) maze with no dead-end at all: a perfectly “braided”
board, so a chased player is never trapped anywhere (the provided analysis script
confirms it with --max-dead-ends 0).

# Not necessary but cute
- add sounds to pathfinder and maze generation
- add maze a second maze solving algorithm
