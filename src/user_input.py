import curses
from .maze import MazeGenerator
from collections.abc import Generator
from typing import cast
from time import sleep
import random
from .maze_utils import (
    generate_maze,
    generate_and_print_matrix,
    print_legend,
    restore_perfect_maze,
    perfect_to_imperfect,
    maze_stats_to_txt,
    solve_maze_path,
)
from . import Configs

Maze = MazeGenerator


def maze_generation_and_stats_to_txt(
    configs: Configs, maze: Maze, stdscr: curses.window
):
    generate_maze(configs, maze, stdscr)
    maze_stats_to_txt(configs, maze, maze.path)


def pathfinder_option(configs: Configs, maze: Maze, stdscr: curses.window):
    solve_maze_path(configs, maze, stdscr)
    maze.generated_path = True
    maze_stats_to_txt(configs, maze, maze.path)


def random_entry_exit(configs: Congigs):
    """Generates two new random values for entry and exit.
    Updates the config dictionary.

    Arg:
        configs: The maze configuration.

    Returns:
        None
    """
    rng = random.Random()  # needed, else randint didn't changed the seed
    for value in ("ENTRY", "EXIT"):
        configs[value] = (
            rng.randint(0, cast(int, configs["WIDTH"]) - 1),
            rng.randint(0, cast(int, configs["HEIGHT"]) - 1),
        )


def new_entry_exit_option(configs: Configs, stdscr: curses.window, maze: Maze):
    """Generates two new random values for entry and exit.
    Updates the config dictionary.
    Checks if the value are valid, else loops itself until it finds
    valid values.

    Args:
        configs: The maze configuration.
        stdscr: The curses window.
        maze: The current maze.

    Returns:
        None
    """
    valid_value: bool = False
    while not valid_value:
        random_entry_exit(configs)
        entry = cast(tuple[int, int], configs["ENTRY"])
        exit = cast(tuple[int, int], configs["EXIT"])
        if configs["ENTRY"] == configs["EXIT"] or (
            maze[entry[0]][entry[1]].ft_logo or maze[exit[0]][exit[1]].ft_logo
        ):
            continue
        maze.entry = entry
        maze.exit = exit
        if maze.generated_path:
            pathfinder_option(configs, maze, stdscr)
        valid_value = True


def refresh_option(maze: Maze, configs: Configs, stdscr: curses.window):
    """Refresh the maze on the stdscr.

    Args:
        maze: The current maze.
        configs: The maze configuration.
        stdscr: The curses window.

    Returns:
        The updated maze.
    """
    stdscr.clear()
    maze.generated_path = False
    valid_entry_exit: bool = False
    while not valid_entry_exit:
        try:
            maze = generate_and_print_matrix(configs, stdscr)
            valid_entry_exit = True
        except ValueError, IndexError:
            random_entry_exit(configs)
    return maze


def increment_decrement_option(
    configs: Configs, key: str, value: int | float, stdscr: curses.window, maze: Maze
):
    """Increment/decrement the value of the config key passed as parameter.

    Args:
        maze: The current maze.
        configs: The maze configuration.
        key: the configs key to incement/decrement.
        value: the increment/decrement amount.
        stdscr: The curses window.

    Returns:
        The updated maze.
    """
    while (ch := stdscr.getch()) in (ord("-"), ord("+"), ord("=")):
        try:
            if ch == ord("-"):
                if key != "SECONDS":
                    configs[key] = cast(int, configs[key]) - value
                else:
                    configs[key] = cast(float, configs[key]) - 0.5
                    if configs[key] < 0.5:
                        configs[key] = 0.5
            elif ch in (ord("+"), ord("=")):
                if key != "SECONDS":
                    configs[key] = cast(int, configs[key]) + value
                else:
                    configs[key] = cast(float, configs[key]) + 0.5
            maze = refresh_option(maze, configs, stdscr)
        except AssertionError:
            configs[key] = cast(int, configs[key]) + value
            maze = refresh_option(maze, configs, stdscr)
    return maze


def ch_parsing(
    ch: int,
    maze: Maze,
    configs: Configs,
    stdscr: curses.window,
    color_pair: Generator[int, None, None],
) -> Maze:
    """Handle keyboard commands and update the maze.

    Args:
        ch: The pressed key.
        maze: The current maze.
        configs: The maze configuration.
        stdscr: The curses window.
        color_pair: The color generator.

    Returns:
        The updated maze.
    """
    if ch == ord("c"):
        configs["PALETTE"] = next(color_pair)
        stdscr.bkgd(" ", cast(int, configs["PALETTE"]))
    elif ch == ord("e"):
        new_entry_exit_option(configs, stdscr, maze)
    elif ch == ord("g"):
        if configs["GEN_ALGORITHM"] == "prim":
            configs["GEN_ALGORITHM"] = "dfs"
        else:
            configs["GEN_ALGORITHM"] = "prim"
        print_legend(stdscr, configs)
    elif ch == ord("h"):
        maze = increment_decrement_option(configs, "WIDTH", 1, stdscr, maze)
        return refresh_option(maze, configs, stdscr)
    elif ch == ord("k"):
        configs["PERFECT"] = not cast(bool, configs["PERFECT"])
        print_legend(stdscr, configs)
        if maze.generated:
            if configs["PERFECT"] == True:
                restore_perfect_maze(configs, maze, stdscr)
                maze_stats_to_txt(configs, maze, maze.path)
            else:
                perfect_to_imperfect(configs, maze, stdscr)
                maze_stats_to_txt(configs, maze, maze.path)
        if maze.generated_path == True:
            solve_maze_path(configs, maze, stdscr)
            maze_stats_to_txt(configs, maze, maze.path)
        else:
            pass
    elif ch == ord("l"):
        return refresh_option(maze, configs, stdscr)
    elif ch == ord("m"):
        maze_generation_and_stats_to_txt(configs, maze, stdscr)
    elif ch == ord("n"):
        pathfinder_option(configs, maze, stdscr)
    elif ch == ord("o"):
        stdscr.clear()
    elif ch == ord("s"):
        maze = increment_decrement_option(configs, "SEED", 1, stdscr, maze)
        maze.path = ""
        maze_generation_and_stats_to_txt(configs, maze, stdscr)
    elif ch == ord("t"):
        maze = increment_decrement_option(configs, "SECONDS", 1, stdscr, maze)
    elif ch == ord("w"):
        return increment_decrement_option(configs, "HEIGHT", 1, stdscr, maze)
    return maze
