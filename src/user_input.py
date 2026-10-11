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

Maze = MazeGenerator


def ch_parsing(
        ch: int,
        maze: Maze,
        configs: Configs,
        stdscr: curses.window,
        color_pair: Generator[int, None, None]
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
    if ch == ord('h'):
        configs['WIDTH'] = cast(int, configs['WIDTH']) + 1
        ch = ord('l')
    elif ch == ord('w'):
        configs['HEIGHT'] = cast(int, configs['HEIGHT']) + 1
        ch = ord('l')
    elif ch == ord('c'):
        configs['PALETTE'] = next(color_pair)
        stdscr.bkgd(' ', cast(int, configs['PALETTE']))
    elif ch == ord('s'):
        configs['SEED'] = cast(int, configs['SEED']) + 1
        stdscr.clear()
        maze = generate_and_print_matrix(configs, stdscr)
        ch = ord('m')
        maze.generated_path = False
    elif ch == ord('d'):
        configs['SECONDS'] = cast(float, configs['SECONDS']) + 0.5
    elif ch == ord('e'):
        valid_value: bool = False
        while not valid_value:
            rng = random.Random() # needed, else randint didn't changed the seed
            for value in ('ENTRY', 'EXIT'):
                configs[value] = (
                        rng.randint(0, cast(int, configs['WIDTH']) - 1),
                        rng.randint(0, cast(int, configs['HEIGHT']) - 1)
                        )
            try:
                assert configs['ENTRY'] != configs['EXIT']
                stdscr.clear()
                maze = generate_and_print_matrix(configs, stdscr)
                maze.generated_path = False
                generate_maze(configs, maze, stdscr)
                valid_value = True
                ch = ord('n')
            except ValueError, AssertionError:
                pass
    elif ch == ord('i'):
        seconds = cast(float, configs['SECONDS'])
        if seconds > 0:
            configs['SECONDS'] = seconds - 0.5
    elif ch == ord('g'):
        if configs['GEN_ALGORITHM'] == 'prim':
            configs['GEN_ALGORITHM'] = 'dfs'
        else:
            configs["GEN_ALGORITHM"] = "prim"
        print_legend(stdscr, configs)
    elif ch == ord('k'):
        configs['PERFECT'] = not cast(bool, configs['PERFECT'])
        print_legend(stdscr, configs)
        if maze.generated:
            if configs['PERFECT'] == True:
                restore_perfect_maze(configs, maze, stdscr)
            else:
                perfect_to_imperfect(configs, maze, stdscr)
        if maze.generated_path == True:
            x = solve_maze_path(configs, maze, stdscr)
            maze_stats_to_txt(configs, maze, x)
        else:
            pass
    elif ch == ord("o"):
        stdscr.clear()
    if ch == ord("l"):
        stdscr.clear()
        maze.generated_path = False
        return generate_and_print_matrix(configs, stdscr)
    elif ch == ord("m"):
        generate_maze(configs, maze, stdscr)
    elif ch == ord('n'):
        x = solve_maze_path(configs, maze, stdscr)
        maze.generated_path = True
        maze_stats_to_txt(configs, maze, x)
    return maze
