import curses
from typing import cast
from collections.abc import Generator
from src import (
    MazeGenerator,
    Configs,
    config_parser,
    init_colors,
    color_generator,
    extend_configs,
    generate_and_print_matrix,
    ch_parsing,
    refresh_option,
)

Maze = MazeGenerator


def a_maze_ing(stdscr: curses.window) -> bool:
    """Run the interactive maze program.

    Args:
        stdscr: The curses window.

    Returns:
        True if a restart is requested, otherwise False.
    """
    configs: Configs = config_parser()
    color_pair: Generator[int, None, None] = color_generator(init_colors())
    configs["PALETTE"] = next(color_pair)
    configs["SECONDS"] = 1
    curses.curs_set(0)  # nascondi il cursore
    stdscr.nodelay(True)  # non blocca su getch()
    extend_configs(configs, stdscr)
    stdscr.bkgd(" ", cast(int, configs["PALETTE"]))
    maze: Maze = generate_and_print_matrix(configs, stdscr)
    rows_cols: tuple[int, int] = stdscr.getmaxyx()
    while ch := stdscr.getch():
        if ch == -1:
            stdscr.timeout(-1)
            continue
        if ch == ord("q"):
            break
        elif ch == ord("r"):
            return True
        maze = ch_parsing(ch, maze, configs, stdscr, color_pair)
        rows_cols2: tuple[int, int] = stdscr.getmaxyx()
        if rows_cols2 != rows_cols:
            maze = refresh_option(maze, configs, stdscr)
        rows_cols = stdscr.getmaxyx()
    return False


def main(stdscr: curses.window) -> None:
    """Loops a_maze_ing for every time the user asks to
    reload starting configuration.

    Args:
        stdscr: curses standard screen
    """
    while a_maze_ing(stdscr):
        stdscr.clear()


def error_handling() -> None:
    import sys
    try:
        curses.wrapper(main)
        return
    except SystemExit:  # ArgumentParser
        print(
            "Invalid number of arguments, only one filename required",
            file=sys.stderr
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
    except IndexError:
        print("Entry and exit must be inside the maze", file=sys.stderr)
    except AssertionError:
        print("Maze can't have less than 2 cells", file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
        import traceback  # da usare solo in development
        traceback.print_exc()
    sys.exit(1)


if __name__ == "__main__":
    error_handling()
