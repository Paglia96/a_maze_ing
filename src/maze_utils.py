from .parser import Configs, extend_configs
from .maze import MazeGenerator, Cell
from typing import cast, Callable
from time import sleep
import curses
from itertools import chain

Maze = MazeGenerator


def restore_perfect_maze(
        configs: Configs, maze: Maze, stdscr: curses.window
        ) -> None:
    """Restore the walls of the perfect maze.

    Args:
        configs: The maze configuration.
        maze: The maze to restore.
        stdscr: The curses window.
    """
    maze.restore_walls(
        stdscr,
        cast(int, configs["PALETTE"]),
        cast(int, configs["HORIZONTAL_OFFSET"]),
        cast(int, configs["VERTICAL_OFFSET"]),
        cast(float, configs["SECONDS"]),
    )


def perfect_to_imperfect(
        configs: Configs, maze: Maze, stdscr: curses.window
        ) -> None:
    """Remove dead ends to make the maze non-perfect.

    Args:
        configs: The maze configuration.
        maze: The maze to modify.
        stdscr: The curses window.
    """
    maze.remove_dead_ends(
        stdscr,
        cast(int, configs["PALETTE"]),
        cast(int, configs["HORIZONTAL_OFFSET"]),
        cast(int, configs["VERTICAL_OFFSET"]),
        cast(float, configs["SECONDS"]),
    )


def maze_stats_to_txt(configs: Configs, maze: Maze, path: str) -> None:
    """Save the maze and its solution to a text file.

    Args:
        configs: The maze configuration.
        maze: The maze to save.
        path: The solution path.
    """
    en = cast(tuple[int, int], configs["ENTRY"])
    ex = cast(tuple[int, int], configs["EXIT"])

    with open(cast(str, configs["OUTPUT_FILE"]), "w") as f:
        for row in maze:
            f.write("".join(f"{cell.walls:x}" for cell in row) + "\n")
        f.write(f"\n{en[0]},{en[1]}          # entry   (x, y)\n")
        f.write(f"{ex[0]},{ex[1]}          # exit   (x, y)")
        f.write(f"\n{path}\n")


def refresh_and_sleep(seconds: float, stdscr: curses.window) -> None:
    """Refresh the screen and wait.

    Args:
        seconds: The time to wait.
        stdscr: The curses window.
    """
    stdscr.refresh()
    sleep(seconds)


def print_matrix(configs: Configs, maze: Maze, stdscr: curses.window) -> None:
    """Draw the maze matrix on the screen.

    Args:
        configs: The maze configuration.
        maze: The maze to draw.
        stdscr: The curses window.
    """

    def print_step(
        configs: Configs,
        maze: Maze,
        stdscr: curses.window,
        print_method: Callable[
            [Cell, curses.window, int, int, int], None
        ],
    ) -> None:
        """Draw all cells using the given method.

        Args:
            configs: The maze configuration.
            maze: The maze to draw.
            stdscr: The curses window.
            print_method: The method used to draw each cell.
        """
        palette = cast(int, configs["PALETTE"])
        horizontal_offset = cast(int, configs["HORIZONTAL_OFFSET"])
        vertical_offset = cast(int, configs["VERTICAL_OFFSET"])

        for cell in chain.from_iterable(maze.get_maze()):
            print_method(
                cell,
                stdscr,
                palette,
                horizontal_offset,
                vertical_offset,
            )
        refresh_and_sleep(0.2, stdscr)

    for print_method in [Maze.Cell.print_base, Maze.Cell.print_self]:
        print_step(configs, maze, stdscr, print_method)
    refresh_and_sleep(0, stdscr)


def print_legend(stdscr: curses.window, configs: Configs) -> None:
    """Display the commands and current settings.

    Args:
        stdscr: The curses window.
        configs: The maze configuration.
    """
    width = cast(int, configs["WIDTH"])
    rows = cast(int, configs["ROWS"])
    cols = cast(int, configs["COLS"])
    amazing = " A_MAZE_ING project from ccrucian and gipaglie "
    legends = [
        "m = generate maze | l = matrix refresh | q = quit | r = reset",
        "n = pathfinder | e = new random entry-exit",
        f"c = color palette | k = Perfect: {configs['PERFECT']}",
        f"g = generation algorithm (current: {configs['GEN_ALGORITHM']})",
        f"p = pathfinder algorithm (current: {configs['SOLVING_ALGORITHM']})",
        "Incrementable/Decrementable options (+/- after pressing option):",
        "w = width | h = height | s = seed | t = speed",
    ]

    maze_height = width * 2 + 1
    maze_top = (rows - maze_height) // 2
    maze_bottom = maze_top + maze_height
    top_y = maze_top // 2
    bottom_y = maze_bottom + (rows - maze_bottom) // 2
    bottom_y -= (len(legends) + 1) // 2
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(bottom_y, (cols - len(" LEGEND ")) // 2, " LEGEND ")
    for legend in legends:
        bottom_y += 1
        legend = legend.center(70)
        stdscr.addstr(bottom_y, (cols - len(legend)) // 2, legend)

    stdscr.addstr(top_y, (cols - len(amazing)) // 2, amazing)
    stdscr.attroff(curses.A_REVERSE)

    refresh_and_sleep(0, stdscr)


def generate_and_print_matrix(configs: Configs, stdscr: curses.window) -> Maze:
    """Create and display a new maze matrix.

    Args:
        configs: The maze configuration.
        stdscr: The curses window.

    Returns:
        The new maze.
    """
    extend_configs(configs, stdscr)
    matrix: Maze = MazeGenerator(configs)
    print_legend(stdscr, configs)
    print_matrix(configs, matrix, stdscr)
    maze_stats_to_txt(configs, matrix, matrix.path)
    return matrix


def generate_maze(configs: Configs, maze: Maze, stdscr: curses.window) -> None:
    """Generate the maze using the selected algorithm.

    Args:
        configs: The maze configuration.
        maze: The maze to generate.
        stdscr: The curses window.
    """
    args: tuple[curses.window, int, int, int, int, float] = (
        stdscr,
        cast(int, configs["PALETTE"]),
        cast(int, configs["HORIZONTAL_OFFSET"]),
        cast(int, configs["VERTICAL_OFFSET"]),
        cast(int, configs["SEED"]),
        cast(float, configs["SECONDS"]),
    )
    if not maze.generated:
        if configs["GEN_ALGORITHM"] == "prim":
            maze.prim_algorithm(*args)
        else:
            maze.dfs(*args)
        maze.generated = True
        if not configs["PERFECT"]:
            perfect_to_imperfect(configs, maze, stdscr)
    refresh_and_sleep(0, stdscr)


def solve_maze_path(
        configs: Configs, maze: Maze, stdscr: curses.window
        ) -> str:
    """Find and display the shortest path.

    Args:
        configs: The maze configuration.
        maze: The maze to solve.
        stdscr: The curses window.

    Returns:
        The solution path.
    """
    path = ""
    if configs["SOLVING_ALGORITHM"] == "bfs":
        path = maze.bfs(stdscr)
    refresh_and_sleep(0, stdscr)
    return path
