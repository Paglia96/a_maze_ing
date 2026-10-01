from src import *
import curses
from src.maze.maze_generator import MazeGenerator

#stdscr.addstr(row + 1, col + 1, '🐭 😿', fg_red_bg_black)
#stdscr.addstr(row + 1, col + 1, '🧀', fg_red_bg_black)
def refresh_and_sleep(seconds: float, stdscr):
    stdscr.refresh()
    sleep(seconds)

def print_legend(stdscr: curses.window, configs: dict):
    legend = "q = quit | c = color palette | g = maze generation algorithm"
    amazing = "A_MAZE_ING project from ccrucian and gipaglie"

    maze_height = configs['WIDTH'] * 2 + 1
    maze_top = (configs['ROWS'] - maze_height) // 2
    maze_bottom = maze_top + maze_height

    top_y = maze_top // 2
    bottom_y = maze_bottom + (configs['ROWS'] - maze_bottom) // 2

    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(bottom_y, (configs['COLS'] - len("LEGEND")) // 2, "LEGEND")
    stdscr.addstr(bottom_y + 1, (configs['COLS'] - len(legend)) // 2, legend)

    stdscr.addstr(top_y, (configs['COLS'] - len(amazing)) // 2, amazing)
    stdscr.attroff(curses.A_REVERSE)
    
    refresh_and_sleep(1, stdscr)

def generate_maze(configs, maze, stdscr: curses.window, color_pairs):
    if configs['GEN_ALGORITHM'] == 'prim':
        maze.prim_algorithm(
                stdscr,
                color_pairs[0],
                configs['HORIZONTAL_OFFSET'],
                configs['VERTICAL_OFFSET'],
                configs['SEED']
                )
    else:
        maze.dfs(
                stdscr,
                color_pairs[0],
                configs['HORIZONTAL_OFFSET'],
                configs['VERTICAL_OFFSET'],
                configs['SEED']
                )
    refresh_and_sleep(1, stdscr)

def print_matrix(configs, maze, stdscr, color_pairs):
    def print_step(configs, maze, stdscr: curses.window, color_pairs, print_method):
        for row, col in product(range(configs['WIDTH']), range(configs['HEIGHT'])):
            print_method(
                maze[row][col],
                stdscr,
                color_pairs[0],
                configs['HORIZONTAL_OFFSET'],
                configs['VERTICAL_OFFSET'],
                )
        refresh_and_sleep(1, stdscr)
    for print_method in [
            MazeGenerator.Cell.print_base,
            MazeGenerator.Cell.print_self
            ]:
        print_step(configs, maze, stdscr, color_pairs, print_method)
    
def maze_stats_to_txt(configs: dict, maze: MazeGenerator):
    with open(configs['OUTPUT_FILE'], 'w') as f:
        for row in range(configs['WIDTH']):
            for col in range(configs['HEIGHT']):
                f.write(f'{maze[row][col].walls:x}')
            f.write('\n')


def inferred_configs(configs, stdscr):
    n_rows, n_cols = stdscr.getmaxyx()
    horizontal_offset: int = (n_cols - (configs['HEIGHT'] * 4 + 1)) // 2
    vertical_offset: int = (n_rows - (configs['WIDTH'] * 2 + 1)) // 2
    configs['ROWS'] = n_rows
    configs['COLS'] = n_cols
    configs['HORIZONTAL_OFFSET'] = horizontal_offset
    configs['VERTICAL_OFFSET'] = vertical_offset

def a_maze_ing(stdscr: curses.window):
    
    configs:dict = config_parser()
    inferred_configs(configs, stdscr)

    color_pairs: list = init_colors()
    curses.curs_set(0) # nascondi il cursore
    stdscr.nodelay(True)  # non blocca su getch()

    stdscr.bkgd(' ', color_pairs[0]) # background base
    print_legend(stdscr, configs) 

   
    maze: list[list[MazeGenerator.Cell]] = MazeGenerator(
            configs['WIDTH'],
            configs['HEIGHT'],
            )
 
    print_matrix(configs, maze, stdscr, color_pairs) 
    generate_maze(configs, maze, stdscr, color_pairs)
    maze_stats_to_txt(configs, maze)
   
    refresh_and_sleep(1, stdscr)
    
    def color_generator(color_pairs: list):
        for color_pair in cycle(color_pairs):
            yield color_pair
    color_pair: Generator = color_generator(color_pairs) 
    while True:
        ch = stdscr.getch() # returna un int
        if ch == ord('q'): # fai il confronto su un int
            break
        elif ch == ord('g'): # maze gen algorithm
            pass
        elif ch == ord('c'):
            color_palette = next(color_pair)
        elif ch == ord('p'):
            pass # find path
            

def main():
    """Main function of the program.
        Prints a matrix, breaks its cells to create a labyrinth and finds the shortest
        path from a randomly genereted starting point to a randomly genereted
        ending point. The all process is animated through curses.

    Args:
        stdscr: curses standard screen
    """
    curses.wrapper(a_maze_ing)
    

if __name__ == "__main__":
    import sys
    try:
        main()
    except SystemExit as e: # ArgumentParser
        print(f'Invalid number of arguments, only one filename required', file=sys.stderr)
    except curses.error:
        print(
                "An error occurred, probably there is "
                "not enough space on the terminal.\n"
                "You can try to solve it:\n"
                "-enlarging the shell window\n"
                "-reducing its screen size (ctrl -)\n"
                "-decrementing the config file variables WIDTH and HEIGHT",
                file=sys.stderr
                )
        sys.exit(1)
    except Exception as e:
        print(e, file=sys.stderr)
        import traceback # da usare solo in development
        traceback.print_exc()
        raise SystemExit(1)
