from src import *
import curses
from src.maze.maze_generator import MazeGenerator
Maze = type[list[list[MazeGenerator.Cell]]]
#stdscr.addstr(row + 1, col + 1, '🐭 😿', fg_red_bg_black)
#stdscr.addstr(row + 1, col + 1, '🧀', fg_red_bg_black)
def refresh_and_sleep(seconds: float, stdscr: curses.window):
    stdscr.refresh()
    sleep(seconds)

def print_legend(stdscr: curses.window, configs: dict):
    amazing = " A_MAZE_ING project from ccrucian and gipaglie "
    legends = [
            'l = matrix refresh | q = quit | r = reset',
            "m = generate maze | "
            f"g = generation algorithm (current: {configs['GEN_ALGORITHM']})",
            "p = pathfinder | "
            f"p = pathfinder algorithm (current: {configs['GEN_ALGORITHM']})",
            "c = color palette | s = change seed | w = width++ | h = height++",
            ]

    maze_height = configs['WIDTH'] * 2 + 1
    maze_top = (configs['ROWS'] - maze_height) // 2
    maze_bottom = maze_top + maze_height

    top_y = maze_top // 2
    bottom_y = maze_bottom + (configs['ROWS'] - maze_bottom) // 2

    stdscr.attron(curses.A_REVERSE)
    bottom_y -= (len(legends) + 1) // 2
    stdscr.addstr(bottom_y, (configs['COLS'] - len(" LEGEND ")) // 2, " LEGEND ")
    for legend in legends:
        bottom_y += 1 
        legend = legend.center(70)
        stdscr.addstr(bottom_y, (configs['COLS'] - len(legend)) // 2, legend)

    stdscr.addstr(top_y, (configs['COLS'] - len(amazing)) // 2, amazing)
    stdscr.attroff(curses.A_REVERSE)
    
    refresh_and_sleep(0, stdscr)

def generate_maze(configs: dict, maze, stdscr: curses.window):
    args: tuple = ( 
            stdscr,
            configs['PALETTE'],
            configs['HORIZONTAL_OFFSET'],
            configs['VERTICAL_OFFSET'],
            configs['SEED']
                )
    if configs['GEN_ALGORITHM'] == 'prim':
        maze.prim_algorithm(*args)
    else:
        maze.dfs(*args)
    refresh_and_sleep(0, stdscr)

def print_matrix(configs: dict, maze, stdscr: curses.window):
    def print_step(configs: dict, maze, stdscr: curses.window, print_method):
        for row, col in product(range(configs['WIDTH']), range(configs['HEIGHT'])):
            print_method(
                maze[row][col],
                stdscr,
                configs['PALETTE'],
                configs['HORIZONTAL_OFFSET'],
                configs['VERTICAL_OFFSET'],
                )
        refresh_and_sleep(0.2, stdscr)
    for print_method in [
            MazeGenerator.Cell.print_base,
            MazeGenerator.Cell.print_self
            ]:
        print_step(configs, maze, stdscr, print_method)
    refresh_and_sleep(0, stdscr)
    
def maze_stats_to_txt(configs: dict, maze: MazeGenerator):
    with open(configs['OUTPUT_FILE'], 'w') as f:
        for row in range(configs['WIDTH']):
            for col in range(configs['HEIGHT']):
                f.write(f'{maze[row][col].walls:x}')
            f.write('\n')


def extend_configs(configs: dict, stdscr: curses.window):
    n_rows, n_cols = stdscr.getmaxyx()
    horizontal_offset: int = (n_cols - (configs['HEIGHT'] * 4 + 1)) // 2
    vertical_offset: int = (n_rows - (configs['WIDTH'] * 2 + 1)) // 2
    configs['ROWS'] = n_rows
    configs['COLS'] = n_cols
    configs['HORIZONTAL_OFFSET'] = horizontal_offset
    configs['VERTICAL_OFFSET'] = vertical_offset

def color_generator(color_pairs: list):
    for color_pair in cycle(color_pairs):
        yield color_pair 

def generate_and_print_matrix(configs, stdscr) -> Maze:
    extend_configs(configs, stdscr)
    print_legend(stdscr, configs) 
    matrix = MazeGenerator(configs['WIDTH'], configs['HEIGHT'])
    print_matrix(configs, matrix, stdscr) 
    return matrix

def ch_parsing(
        ch: int,
        maze: Maze,
        configs: dict,
        stdscr,
        color_pair: Generator
        ) -> Maze:
    if ch == ord('h'):
        configs['WIDTH'] += 1
        ch = ord('l')
    elif ch == ord('w'):
        configs['HEIGHT'] += 1
        ch = ord('l')
    elif ch == ord('c'):
        configs['PALETTE'] = next(color_pair)
        stdscr.bkgd(' ', configs['PALETTE'])
    elif ch == ord('p'):
        pass
    elif ch == ord('s'):
        configs['SEED'] += 1
        maze = generate_and_print_matrix(configs, stdscr)
        ch = ord('m')
    elif ch == ord('g'):
        if configs['GEN_ALGORITHM'] == 'prim':
            configs['GEN_ALGORITHM'] = 'dfs'
        else:
            configs['GEN_ALGORITHM'] = 'prim'
        print_legend(stdscr, configs)
    elif ch == ord('o'):
        stdscr.clear()
    if ch == ord('l'):
        stdscr.clear()
        return generate_and_print_matrix(configs, stdscr)
    elif ch == ord('m'):
        generate_maze(configs, maze, stdscr)
        maze_stats_to_txt(configs, maze)
    return maze

def a_maze_ing(stdscr: curses.window) -> bool:
    """Prints a matrix, breaks its cells to create a labyrinth and finds the shortest
    path from a randomly genereted starting point to a randomly genereted
    ending point. The all process is animated through curses.

    Parameter:
        stdscr: curses standard screen
    """
    configs:dict = config_parser()
    color_pair: Generator = color_generator(init_colors()) 
    configs['PALETTE'] = next(color_pair)
    curses.curs_set(0) # nascondi il cursore
    stdscr.nodelay(True)  # non blocca su getch()
    width, height = (configs['WIDTH'], configs['HEIGHT'])
    extend_configs(configs, stdscr)
    stdscr.bkgd(' ', configs['PALETTE'])
    maze: Maze = generate_and_print_matrix(configs, stdscr)
    while (ch := stdscr.getch()):
        if ch == ord('q'):
            break
        elif ch == ord('r'):
            return True
        maze = ch_parsing(ch, maze, configs, stdscr, color_pair)
    return False

def main(stdscr: curses.window) -> None:
    """Loops a_maze_ing for every time the user asks to reload starting configuration.

    Parameter:
        stdscr: curses standard screen
    """
    while a_maze_ing(stdscr):
        stdscr.clear()
    

if __name__ == "__main__":
    import sys
    try:
        curses.wrapper(main)
    except SystemExit as e: # ArgumentParser
        print(
            f'Invalid number of arguments, only one filename required',
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
                file=sys.stderr
                )
        sys.exit(1)
    except Exception as e:
        print(e, file=sys.stderr)
        import traceback # da usare solo in development
        traceback.print_exc()
        raise SystemExit(1)
