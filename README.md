_This project has been created as part of the 42 curriculum by ccrucian, gipaglie_

# A-Maze-ing

## Description

**A-Maze-ing** is a project from the 42 curriculum focused on generating, displaying, and solving mazes.

The program reads its parameters from a configuration file, generates a random maze, finds a path from the entrance to the exit, and saves the result in an output file using the format required by the project.

The main objectives of this project are:

- understanding and implementing maze-generation algorithms;
- representing a grid as a graph;
- finding the shortest path between two cells;
- handling configuration and output files;
- applying modular programming principles;
- displaying the maze and its solution in the terminal.

### Features

- Random maze generation.
- Support for perfect and imperfect mazes.
- Custom maze width and height.
- Configurable entrance and exit coordinates.
- Optional `42` pattern generation when the maze is large enough.
- Shortest-path search between the entrance and exit.
- ASCII maze visualization.
- Optional display of the solution path.
- Export of the maze to the output file specified in the configuration.
- Support for a seed to make results reproducible.

### Algorithms

Maze generation is based on:
- **Depth-First Search**, implemented with a backtracking algorithm. The algorithm visits unvisited cells and removes the walls between adjacent cells.
This algorithm has been choosen as it is a standard in the graph theory.
- **Prim**. The algorithm visits unvisited cells and removes the walls between adjacent cells.
This algorithm has been choosen as it is a standard choice in computer maze generation.

Maze solving is based on:
- **Breadth-First Search**. Since every movement has the same cost, BFS can be used to find the shortest path between the entrance and the exit.
This algorithm has been choosen as it is a standard in the graph theory.

### Reusable code
- The parsing file is reusable changing the parameters received by the config dictionary.
It requires a config file that contains key-value pairs in the format 'KEY=VALUE'.
- The maze python module is reusable but requires to delete curses dependencies if not necessary. It can generate a maze starting from a grid and find the shortest path from an entry point to an exit one.
How to use it:

## Requirements

- Python 3.10 or newer
- `pip`
- `make`

The required Python version may vary depending on the project configuration.

## Instructions

### Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Create and activate python virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```bash
make install
```

### Check lint errors
```bash
make lint
```


### Run the program
```bash
make run
```
Follow the instructions printed on the terminal screen with curses

## Resources
### Algorithms documentation
#### [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [DFS: Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)
- [PRIM](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
#### [Maze-solving Algorithms](https://en.wikipedia.org/wiki/Maze-solving_algorithm)
- [BFS: Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

### Python general documentation
- [Python docs](https://docs.python.org/3/)
- [Packaging](https://packaging.python.org/)
- [Venv](https://docs.python.org/3/library/venv.html)

### Role of each team member
- gipaglie: parsing of the config file, first implementation of the MazeGenerator class and the drawing of the matrix-maze with curses, prim algorithm
- ccrucian: dfs and bfs algorithms, additions and changes to the project
The collaboration was done using git, giving both member the ability to improve the knowledge of this control version software.



### AI Usage
Artificial intelligence tools were used as development support, not as a replacement for understanding or writing the code.

AI was used for:
- comparing possible maze-generation and maze-solving strategies;
- suggesting a modular project structure;
- reviewing and formatting this README.md;
- identifying possible edge cases to test;
- improving the clarity of comments and documentation.

The final code was reviewed, adapted, tested, and understood by the project authors in accordance with the rules of 42.
