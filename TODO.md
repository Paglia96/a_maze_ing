# Urgent
- print to file solving algorithm sequence and test the result with moulinette(implemneted must be tested with moulinette): da testare anche la flag scritta sotto nella sezione bonus
- Show/Hide a valid shortest path from the entrance to the exit. (just put a default flag parameter in print self hide=False that prints 3 spaces if True)
- The “42” pattern may be omitted in case the maze size does not allow
it (i.e.too small). Print an error message on the console in that
case: lo printiamo su curses, perche' i print sul terminale non si vedono quando siamo su curses. Pero' lascerei creare comunque il labirinto senza 42...me l'ero perso ahahahahah

# To do at the end of the project:
- generic error handling in main
- remove import traceback
- linting
- Complete the readme
- Togliere runcarli dal makefile

# MazeGenerator
You must provide a short documentation describing how to:
Instantiate and use your generator, with at least a basic example.
Pass custom parameters (e.g., size, seed).
Access the generated structure, and access at least a solution.
This entire reusable module (code and documentation) must be available in a single file suitable for a later installation by pip.
This package must be called mazegen-* and the file must be located at the root of your
git repository.
It will be asked during the evaluation: in a virtualenv or equivalent, install the needed tools and build your package again from your sources.

# Bonus
A default (non-perfect) maze with no dead-end at all: a perfectly “braided”
board, so a chased player is never trapped anywhere (the provided analysis script
confirms it with --max-dead-ends 0).

# Not necessary but cute
- add sounds to pathfinder and maze generation
- add maze a second maze solving algorithm
