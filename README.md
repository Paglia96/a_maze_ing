*This project has been created as part of the 42 curriculum by ccrucian, gipaglie.*

# A-Maze-ing

## Description

**A-Maze-ing** is a Python maze generator, visualizer, and solver.

The program reads a configuration file, builds a random maze, displays it in the terminal, optionally solves it, and writes the maze data to an output file using the hexadecimal wall format required by the subject.

The project focuses on:

- parsing a configuration file;
- generating valid mazes from a grid of cells;
- supporting perfect and imperfect mazes;
- representing each cell as a set of walls;
- finding a shortest path from entry to exit;
- displaying the maze interactively in the terminal;
- keeping the maze generation logic reusable through a Python package.

## Features

- Random maze generation with a reproducible seed.
- Two generation algorithms: Prim and DFS.
- Perfect maze mode with a single path between cells.
- Imperfect mode that opens extra walls to create loops and reduce dead ends.
- BFS shortest-path solving.
- Terminal visualization with `curses`.
- Animated generation and pathfinding.
- Show/hide solution path.
- Change wall colors while the program is running.
- Generate new random entry and exit coordinates.
- Optional `42` pattern made of closed cells when the maze is large enough.
- Export to the subject output format.

## Instructions

### Requirements

- Python 3.11.15 or newer, as declared in the project files.
- `pip`
- `make`

The project has no external runtime dependency.

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

For editable development:

```bash
make install-dev
```

### Run

```bash
python3 a_maze_ing.py config.txt
```

or:

```bash
make run
```

The program expects exactly one argument: the path to a configuration file.

### Makefile Rules

- `make install`: installs the project package.
- `make install-dev`: installs the project in editable mode.
- `make build`: builds the package distribution files.
- `make run`: runs `a_maze_ing.py config.txt`.
- `make debug`: runs the program with `pdb`.
- `make clean`: removes generated caches and build artifacts.
- `make lint`: runs `flake8` and `mypy` with the required subject flags.
- `make lint-strict`: runs `flake8` and `mypy --strict`.
- `make auto-lint`: formats the code with `ruff` and `black`.

## Configuration File

The configuration file contains one `KEY=VALUE` pair per line.
Lines beginning with `#` are ignored, and inline comments after `#` are also accepted.

### Mandatory Keys

```txt
WIDTH=9
HEIGHT=9
ENTRY=3,0
EXIT=7,7
OUTPUT_FILE=maze.txt
PERFECT=TRUE
```

- `WIDTH`: maze width in cells.
- `HEIGHT`: maze height in cells.
- `ENTRY`: entry coordinates as `x,y`.
- `EXIT`: exit coordinates as `x,y`.
- `OUTPUT_FILE`: output file path.
- `PERFECT`: `TRUE` or `FALSE`.

### Optional Keys

```txt
SEED=10
GEN_ALGORITHM=prim
SOLVING_ALGORITHM=bfs
```

- `SEED`: integer seed used for reproducible generation.
- `GEN_ALGORITHM`: `prim` or `dfs`.
- `SOLVING_ALGORITHM`: currently `bfs`.

If optional keys are missing, the parser applies defaults:

- `SEED=1`
- `GEN_ALGORITHM=prim`
- `SOLVING_ALGORITHM=bfs`

## Interactive Controls

While the program is running:

- `m`: generate the maze.
- `n`: show or hide the shortest path.
- `c`: change the color palette.
- `e`: generate new random entry and exit coordinates.
- `g`: switch generation algorithm between Prim and DFS.
- `k`: toggle perfect/imperfect mode.
- `l`: refresh the matrix.
- `r`: reset from the starting configuration.
- `q`: quit.
- `w`, `h`, `s`, `t`: select width, height, seed, or animation speed.
- `+` / `-`: increment or decrement the selected option.

## Output File Format

The generated maze is written to the configured output file.

Each maze cell is encoded with one hexadecimal digit. Each bit represents a closed wall:

| Bit | Direction |
| --- | --- |
| 0 | North |
| 1 | East |
| 2 | South |
| 3 | West |

A closed wall sets the bit to `1`; an open wall sets it to `0`.

Examples:

- `3` is binary `0011`: north and east are closed, south and west are open.
- `a` is binary `1010`: east and west are closed, north and south are open.

The file contains:

1. One maze row per line.
2. An empty line.
3. Entry coordinates.
4. Exit coordinates.
5. The shortest path, using `N`, `E`, `S`, and `W`.

Example:

```txt
911151113
ac2a9446a
afaaafffa

3,0          # entry   (x, y)
7,7          # exit   (x, y)
EESSWWNN
```

## Algorithms

### Maze Generation

The project implements two generation algorithms.

**Prim**

Prim is the default generation algorithm. It starts from a random valid cell, repeatedly chooses a frontier cell, opens a wall toward an unvisited neighbour, and grows the maze until all valid cells are connected.

This algorithm was chosen because it is a classic graph algorithm, it naturally produces connected mazes, and it fits well with the subject requirement that maze generation should be random and reproducible with a seed.

**Depth-First Search**

DFS is implemented with a backtracking stack. It explores one branch until it cannot continue, then backtracks and opens another valid path.

This algorithm was added because it is another standard maze-generation method, easy to compare with Prim, and useful for demonstrating multiple generation strategies.

### Maze Solving

The solver uses **Breadth-First Search**.

BFS was chosen because each move in the maze has the same cost. For an unweighted grid, BFS guarantees a shortest path from entry to exit when a path exists.

## Reusable Code

The reusable part of the project is the maze package in `src/maze`, centered around the `MazeGenerator` class.

It can be imported by another Python project after installing the package. It exposes:

- the maze matrix through `get_maze()`;
- cell wall information through each `Cell`;
- generation methods such as `prim_algorithm()` and `dfs()`;
- pathfinding through `bfs()`;
- helper methods for coordinates, wall handling, and maze structure access.

The constructor creates a grid with all walls closed. Call a generation method before accessing the generated maze or solving it. The current API requires a `curses` window for both generation and solving, even when animation is disabled with `SECONDS=0.0`.

After installing the package, the following example generates a maze and returns its cells and shortest solution path:

```python
import curses

from maze import MazeGenerator


def generate(stdscr):
    configs = {
        "WIDTH": 9,
        "HEIGHT": 9,
        "ENTRY": (0, 0),
        "EXIT": (8, 8),
        "PERFECT": True,
        "SEED": 10,
        "PALETTE": 0,
        "HORIZONTAL_OFFSET": 1,
        "VERTICAL_OFFSET": 1,
        "SECONDS": 0.0,
    }

    maze = MazeGenerator(configs)
    rows, columns = stdscr.getmaxyx()
    if rows < maze.width * 2 + 3 or columns < maze.height * 4 + 3:
        raise ValueError("Enlarge the terminal or reduce the maze size.")

    stdscr.clear()
    for row in maze.get_maze():
        for cell in row:
            cell.print_base(stdscr, 0, 1, 1)

    maze.prim_algorithm(stdscr, 0, 1, 1, configs["SEED"], 0.0)
    if not configs["PERFECT"]:
        maze.remove_dead_ends(stdscr, 0, 1, 1, 0.0)

    solution = maze.bfs(stdscr, hide=True)
    return maze.get_maze(), solution


matrix, solution = curses.wrapper(generate)
wall_masks = [[int(cell.walls) for cell in row] for row in matrix]
print("Wall masks:", wall_masks)
print("Shortest path:", solution)
```

Change `SEED` to select another reproducible maze. To use DFS, replace the `prim_algorithm()` call with `dfs()` using the same arguments. For an imperfect maze, set `PERFECT` to `False`; the example explicitly calls `remove_dead_ends()` after generation because the generation methods do not apply this setting automatically.

For direct use of the current class, `WIDTH` counts matrix rows, `HEIGHT` counts columns, and `ENTRY` and `EXIT` use `(row, column)` indices. These internal conventions differ from the configuration file's intended `(x, y)` coordinates. When changing the dimensions, update the exit indices and keep both endpoints outside the closed `42` cells. The example requires a terminal of at least 21 rows and 39 columns.

`get_maze()` returns the cell matrix. Each `Cell.walls` is a bitmask with the North, East, South, and West bits described in the output format section; `wall_masks` above converts these masks to integers. `bfs()` returns the shortest path as a string of `N`, `E`, `S`, and `W` moves and also stores it in `maze.path`. Its `hide=True` argument hides the path while preserving the returned solution. These direct calls do not write an output file.

`curses.wrapper()` initializes the terminal and restores it before the results are printed. A future application using another display layer would need to adapt the drawing calls in the current generation and solving methods.

The package metadata is defined in `pyproject.toml` as `mazegen`. A distributable package can be built with:

```bash
make build
```

## Project Structure

```txt
.
|-- a_maze_ing.py              # main program
|-- config.txt                 # default configuration file
|-- maze.txt                   # generated output file
|-- Makefile
|-- pyproject.toml
|-- LICENSE
`-- src
    |-- parser.py              # config parsing and validation
    |-- user_input.py          # interactive commands
    |-- maze_utils.py          # display, generation, solving, output helpers
    |-- curses_colors.py       # terminal color palettes
    `-- maze
        |-- cell.py            # Cell and Wall definitions
        |-- maze_generator.py  # MazeGenerator class
        |-- algorithms.py      # Prim, DFS, BFS
        |-- algorithms_utils.py
        `-- logos.py           # 42 pattern coordinates
```

## Team And Project Management

### Roles

- `gipaglie`: configuration parsing, first implementation of the `MazeGenerator` class, first curses matrix drawing, Prim algorithm.
- `ccrucian`: DFS generation, BFS solving, project integration, refactoring, linting, documentation improvements.

### Planning

The anticipated plan was:

1. Parse and validate the configuration file.
2. Build a cell-based maze model.
3. Implement one generation algorithm.
4. Add output-file export.
5. Add terminal visualization.
6. Add shortest-path solving.
7. Add optional features and cleanup.

During development the plan evolved: the team added a second generation algorithm, interactive controls, color palettes, animation, seed handling, and a reusable package structure.

### What Worked Well

- Splitting the project into parsing, generation, display, and input modules made the code easier to evolve.
- Using a `Wall` bitmask kept the output format close to the internal representation.
- Git helped both team members work on separate parts and merge improvements.
- Type hints and linting helped catch inconsistencies while refactoring.

### What Could Be Improved

- Add automated tests for the parser, wall consistency, path validity, and output format.
- Decouple the generation algorithms further from `curses` so the reusable module can be used without a terminal UI.
- Add a stricter validation step against the subject analyzer.
- Generate both `.whl` and `.tar.gz` artifacts before final evaluation.

### Tools Used

- Git for collaboration and version control.
- `make` for project commands.
- `flake8`, `mypy`, `ruff`, and `black` for code quality.
- Python virtual environments for local isolation.

## Resources

### Algorithms

- [Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Maze-solving algorithm](https://en.wikipedia.org/wiki/Maze-solving_algorithm)

### Python

- [Python documentation](https://docs.python.org/3/)
- [curses documentation](https://docs.python.org/3/library/curses.html)
- [venv documentation](https://docs.python.org/3/library/venv.html)
- [Python packaging guide](https://packaging.python.org/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)

### AI Usage

AI tools were used as development support, not as a replacement for understanding the project.

AI was used for:

- comparing maze generation and maze solving strategies;
- discussing edge cases for parsing and maze validity;
- improving the modular organization of the project;
- reviewing documentation wording;
- preparing and formatting this README.

The final code was reviewed, adapted, tested, and understood by the project authors.
