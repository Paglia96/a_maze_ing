import curses
from typing import cast
from itertools import chain, cycle
from collections.abc import Generator, Callable
from time import sleep

from src.maze import MazeGenerator
from src.parser import Configs, config_parser
from src.curses_colors import init_colors

Maze = MazeGenerator


def refresh_and_sleep(
        seconds: float, stdscr: curses.window
        ) -> None:
    """Refresh the screen and wait.

    Args:
        seconds: The time to wait.
        stdscr: The curses window.
    """
    stdscr.refresh()
    sleep(seconds)


def print_legend(
        stdscr: curses.window, configs: Configs) -> None:
    """Display the commands and current settings.

    Args:
        stdscr: The curses window.
        configs: The maze configuration.
    """
    width = cast(int, configs['WIDTH'])
    rows = cast(int, configs['ROWS'])
    cols = cast(int, configs['COLS'])
    amazing = " A_MAZE_ING project from ccrucian and gipaglie "
    legends = [
            'l = matrix refresh | q = quit | r = reset',
            "m = generate maze | d = speed-- | i = speed++",
            "n = pathfinder | e = new random entry-exit",
            "g = generation algorithm "
            f"(current: {configs['GEN_ALGORITHM']})",
            "p = pathfinder algorithm "
            f"(current: {configs['SOLVING_ALGORITHM']})",
            f"k = Perfect: {configs['PERFECT']}",
            "c = color palette | s = change seed | w = width++ | h = height++",
            ]

    maze_height = width * 2 + 1
    maze_top = (rows - maze_height) // 2
    maze_bottom = maze_top + maze_height
    top_y = maze_top // 2
    bottom_y = maze_bottom + (rows - maze_bottom) // 2
    stdscr.attron(curses.A_REVERSE)
    bottom_y -= (len(legends) + 1) // 2
    stdscr.addstr(bottom_y, (cols - len(" LEGEND ")) // 2, " LEGEND ")
    for legend in legends:
        bottom_y += 1
        legend = legend.center(70)
        stdscr.addstr(bottom_y, (cols - len(legend)) // 2, legend)

    stdscr.addstr(top_y, (cols - len(amazing)) // 2, amazing)
    stdscr.attroff(curses.A_REVERSE)

    refresh_and_sleep(0, stdscr)


def generate_maze(
        configs: Configs, maze: Maze, stdscr: curses.window
        ) -> None:
    """Generate the maze using the selected algorithm.

    Args:
        configs: The maze configuration.
        maze: The maze to generate.
        stdscr: The curses window.
    """
    args: tuple[
        curses.window, int, int, int, int, float
        ] = ( 
            stdscr,
            cast(int, configs['PALETTE']),
            cast(int, configs['HORIZONTAL_OFFSET']),
            cast(int, configs['VERTICAL_OFFSET']),
            cast(int, configs['SEED']),
            cast(float, configs['SECONDS'])
                )
    if not maze.generated:
        if configs['GEN_ALGORITHM'] == 'prim':
            maze.prim_algorithm(*args)
        else:
            maze.dfs(*args)
        maze.generated = True
        if not configs["PERFECT"]:
            perfect_to_imperfect(configs, maze, stdscr)
    refresh_and_sleep(0, stdscr)


def print_matrix(
        configs: Configs, maze: Maze, stdscr: curses.window
        ) -> None:
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
                [MazeGenerator.Cell, curses.window, int, int, int],
                None
            ]
            ) -> None:
        """Draw all cells using the given method.

        Args:
            configs: The maze configuration.
            maze: The maze to draw.
            stdscr: The curses window.
            print_method: The method used to draw each cell.
        """
        palette = cast(int, configs['PALETTE'])
        horizontal_offset = cast(int, configs['HORIZONTAL_OFFSET'])
        vertical_offset = cast(int, configs['VERTICAL_OFFSET'])

        for cell in chain.from_iterable(maze.get_maze()):
            print_method(
                cell,
                stdscr,
                palette,
                horizontal_offset,
                vertical_offset,
                )
        refresh_and_sleep(0.2, stdscr)

    for print_method in [MazeGenerator.Cell.print_base, MazeGenerator.Cell.print_self]:
        print_step(configs, maze, stdscr, print_method)
    refresh_and_sleep(0, stdscr)


def maze_stats_to_txt(
        configs: Configs, maze: Maze, path: str) -> None:
    """Save the maze and its solution to a text file.

    Args:
        configs: The maze configuration.
        maze: The maze to save.
        path: The solution path.
    """
    filename = cast(str, configs['OUTPUT_FILE'])
    width = cast(int, configs['WIDTH'])
    height = cast(int, configs['HEIGHT'])

    entry = cast(tuple[int, int], configs['ENTRY'])
    exit = cast(tuple[int, int], configs['EXIT'])
    

    with open(filename, 'w') as f:
        for row in maze:
            f.write("".join(f"{cell.walls:x}" for cell in row) + "\n")
        #f.write(
        #        f"{entry[0]}, "
        #        f"{entry[1]}"
        #        ' ' * 5 + '# entry   (x, y)'
        #        )
        #f.write(
        #        f"{exit[0]}, "
        #        f"{exit[1]}"
        #        ' ' * 5 + '# exit   (x, y)'
        #        )
        #f.write(f'\n{configs['SOLUTION']}\n')
        f.write(f"\n{path}")


def extend_configs(
        configs: Configs, stdscr: curses.window) -> None:
    """Update the screen size and maze offsets.

    Args:
        configs: The maze configuration.
        stdscr: The curses window.
    """
    width = cast(int, configs['WIDTH'])
    height = cast(int, configs['HEIGHT'])
    n_rows, n_cols = stdscr.getmaxyx()
    horizontal_offset: int = (n_cols - (height * 4 + 1)) // 2
    vertical_offset: int = (n_rows - (width * 2 + 1)) // 2
    configs['ROWS'] = n_rows
    configs['COLS'] = n_cols
    configs['HORIZONTAL_OFFSET'] = horizontal_offset
    configs['VERTICAL_OFFSET'] = vertical_offset


def color_generator(
        color_pairs: list[int]
        ) -> Generator[int, None, None]:
    """Generate color pairs in a continuous cycle.

    Args:
        color_pairs: The list of color pairs.

    Yields:
        The next color pair.
    """
    from itertools import cycle
    for color_pair in cycle(color_pairs):
        yield color_pair


def generate_and_print_matrix(
        configs: Configs, stdscr: curses.window
        ) -> Maze:
    """Create and display a new maze matrix.

    Args:
        configs: The maze configuration.
        stdscr: The curses window.

    Returns:
        The new maze.
    """
    extend_configs(configs, stdscr)
    matrix = MazeGenerator(configs)
    print_legend(stdscr, configs)
    print_matrix(configs, matrix, stdscr)
    return matrix


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
        cast(int, configs['PALETTE']),
        cast(int, configs['HORIZONTAL_OFFSET']),
        cast(int, configs['VERTICAL_OFFSET']),
        cast(float, configs['SECONDS'])
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
        cast(int, configs['PALETTE']),
        cast(int, configs['HORIZONTAL_OFFSET']),
        cast(int, configs['VERTICAL_OFFSET']),
        cast(float, configs['SECONDS'])
        )


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
    elif ch == ord('n'):
        x = solve_maze_path(configs, maze, stdscr)
        maze.generated_path = True
        maze_stats_to_txt(configs, maze, x)
    elif ch == ord('s'):
        configs['SEED'] = cast(int, configs['SEED']) + 1
        stdscr.clear()
        maze = generate_and_print_matrix(configs, stdscr)
        ch = ord('m')
        maze.generated_path = False
    elif ch == ord('d'):
        configs['SECONDS'] = cast(float, configs['SECONDS']) + 0.5
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
    return maze


def a_maze_ing(stdscr: curses.window) -> bool:
    """Run the interactive maze program.

    Args:
        stdscr: The curses window.

    Returns:
        True if a restart is requested, otherwise False.
    """
    configs: Configs = config_parser()
    color_pair: Generator[int, None, None] = color_generator(init_colors()) 
    configs['PALETTE'] = next(color_pair)
    configs['SECONDS'] = 1
    curses.curs_set(0) # nascondi il cursore
    stdscr.nodelay(True)  # non blocca su getch()
    width, height = (configs["WIDTH"], configs["HEIGHT"])
    extend_configs(configs, stdscr)
    stdscr.bkgd(' ', cast(int, configs['PALETTE']))
    maze: Maze = generate_and_print_matrix(configs, stdscr)
    while ch := stdscr.getch():
        if ch == -1:
            curses.napms(10)
            continue
        if ch == ord("q"):
            break
        elif ch == ord("r"):
            return True
        maze = ch_parsing(ch, maze, configs, stdscr, color_pair)
    return False


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
    if configs['SOLVING_ALGORITHM'] == 'bfs':
        path = maze.bfs(stdscr)
    refresh_and_sleep(0, stdscr)
    return path


def main(stdscr: curses.window) -> None:
    """Loops a_maze_ing for every time the user asks to reload starting configuration.

    Args:
        stdscr: curses standard screen
    """
    while a_maze_ing(stdscr):
        stdscr.clear()


if __name__ == "__main__":
    import sys

    try:
        curses.wrapper(main)
    except SystemExit:  # ArgumentParser
        print(
            f"Invalid number of arguments, only one filename required", file=sys.stderr
        )
    except curses.error:
        print(
            "An error occurred, probably there is "
            "not enough space on the terminal.\n"
            "You can try to solve it:\n"
            "-enlarging the shell window\n"
            "-reducing its screen size (ctrl -)\n"
            "-decrementing the config file variables WIDTH and HEIGHT",
            file=sys.stderr,
        )
        sys.exit(1)
    except IndexError:
        print("Entry and exit must be inside the maze", file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
        import traceback  # da usare solo in development

        traceback.print_exc()
        raise SystemExit(1)
