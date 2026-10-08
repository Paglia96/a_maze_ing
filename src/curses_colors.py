import curses

def init_colors() -> list[int]:
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
