from src import *
import curses as c
from src.maze.maze_generator import MazeGenerator

#stdscr.addstr(row + 1, col + 1, '🐭', palette)
#stdscr.addstr(row + 1, col + 1, '🧀', palette)
def print_legend(stdscr, n_cols, n_rows, width, height):
    legend = "q = quit | and | other | commands"
    amazing = "A_MAZE_ING project from ccrucian and gipaglie"

    maze_height = width * 2 + 1
    maze_top = (n_rows - maze_height) // 2
    maze_bottom = maze_top + maze_height

    top_y = maze_top // 2
    bottom_y = maze_bottom + (n_rows - maze_bottom) // 2

    stdscr.attron(c.A_REVERSE)
    stdscr.addstr(bottom_y, (n_cols - len("LEGEND")) // 2, "LEGEND")
    stdscr.addstr(bottom_y + 1, (n_cols - len(legend)) // 2, legend)

    stdscr.addstr(top_y, (n_cols - len(amazing)) // 2, amazing)
    stdscr.attroff(c.A_REVERSE)

def main(stdscr: c.window):
    configs:dict = config_parser()
    width: int = configs['WIDTH'] 
    height: int = configs['HEIGHT']
    
    c.curs_set(0) # nascondi il cursore
    stdscr.nodelay(True)  # non blocca su getch()
    c.start_color()
    n_rows, n_cols = stdscr.getmaxyx()
    horizontal_offset: int = (n_cols - (height * 4 + 1)) // 2
    vertical_offset: int = (n_rows - (width * 2 + 1)) // 2
    c.init_pair(1, c.COLOR_RED, c.COLOR_BLACK)
    c.init_pair(2, c.COLOR_RED, c.COLOR_BLACK)
    palette: int = c.color_pair(1)
    stdscr.bkgd(' ', c.color_pair(2)) # background base

    print_legend(stdscr, n_cols, n_rows, width, height)
    stdscr.refresh()
    sleep(1)   

    maze: list[list[MazeGenerator.Cell]] = MazeGenerator(width, height).maze
    
    for row, col in product(range(width), range(height)):
        maze[row][col].print_base(stdscr, palette, horizontal_offset, vertical_offset)

    stdscr.refresh()
    sleep(1)

    for row, col in product(range(width), range(height)):
        maze[row][col].print_self(stdscr, palette, horizontal_offset, vertical_offset)

    while True:
        ch = stdscr.getch() # returna un int
        if ch == ord('q'): # fai il confronto su un int
            break

if __name__ == "__main__":
    from sys import stderr
    try:
        c.wrapper(main)
    except SystemExit as e: # ArgumentParser
        print(f'Invalid number of arguments, only one filename required', file=stderr)
    except c.error:
        print(
                "An error occurred, probably there is "
                "not enough space on the terminal.\n"
                "You can try to solve it:\n"
                "-enlarging the shell window\n"
                "-reducing its screen size (ctrl -)\n"
                "-decrementing the config file variables WIDTH and HEIGHT",
                file=stderr
                )
        raise SystemExit(1) 
    except Exception as e:
        print(e, file=stderr)
        import traceback # da usare solo in development
        traceback.print_exc()
        raise SystemExit(1)
