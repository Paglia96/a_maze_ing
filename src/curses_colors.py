import curses
from collections.abc import Generator


def color_generator(color_pairs: list[int]) -> Generator[int, None, None]:
    """Generate color pairs in a continuous cycle.

    Args:
        color_pairs: The list of color pairs.

    Yields:
        The next color pair.
    """
    from itertools import cycle

    for color_pair in cycle(color_pairs):
        yield color_pair


def init_colors() -> list[int]:
    """Initialize curses color pairs.

    Returns:
    A list of color pairs used to draw the maze.
    """
    curses.start_color()
    colors = [
        (curses.COLOR_RED, curses.COLOR_BLACK),
        (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        (curses.COLOR_GREEN, curses.COLOR_BLACK),
        (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        (curses.COLOR_BLUE, curses.COLOR_BLACK),
        (curses.COLOR_CYAN, curses.COLOR_BLACK),
        (curses.COLOR_WHITE, curses.COLOR_BLACK),
    ]
    color_pairs = []
    for color_pair, (fg, bg) in enumerate(colors, start=1):
        curses.init_pair(color_pair, fg, bg)
        color_pairs.append(curses.color_pair(color_pair))
    return color_pairs
