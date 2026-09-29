import curses as c
from time import sleep
from enum import IntFlag
from dataclasses import dataclass, field
from itertools import product
from typing import Callable
from random import seed, choice, randint

class MazeGenerator:
    """Represents the Maze and offers tools to work with it.

    Attributes:
        width: width of the labyrinth
        height: height of the labirinth
        maze: the labirinth
    """
    class Wall(IntFlag):
        """Represent wall states as bitmask values.

        Each bit indicates whether a wall is closed:

        * ``1``: the wall is closed.
        * ``0``: the wall is open.

        The values can be combined as bitmasks:

        * ``0xF`` (15): all walls are closed.
        * ``0x3`` (3): the upper and left walls are closed.
        """

        UP = 1 # 0001
        RIGHT = 2 # 0010
        DOWN = 4 # 0100
        LEFT = 8 # 1000

        def opposite_wall(self) -> "MazeGenerator.Wall":
            """Receives a single wall and returns its reversed value"""
            if self == type(self).UP:
                return type(self).DOWN
            if self == type(self).DOWN:
                return type(self).UP
            if self == type(self).LEFT:
                return type(self).RIGHT
            if self == type(self).RIGHT:
                return type(self).LEFT
            
    @dataclass
    class Cell:
        """Represent a cell of the maze.

        Attributes:
            x: row position in the matrix
            y: column position in the matrix
            width: total width of the matrix
            height: total height of the matrix
            walls: instance of the Wall class
        """
        x: int
        y: int
        width: int
        height: int
        walls: "MazeGenerator.Wall" = field(
                default_factory=lambda: MazeGenerator.Wall(0xF)
                )
        is_visited: bool = False
        entry: bool = False
        end: bool = False

        def adjacent_cell(self, wall: str):
            """Based on the cell wall received,
            returns the coordinates of the adjacent cell"""
            match wall:
                case 'UP':
                    return (self.x - 1, self.y)
                case 'LEFT':
                    return (self.x, self.y - 1)
                case 'RIGHT':
                    return (self.x, self.y + 1)
                case 'DOWN':
                    return (self.x + 1, self.y)
        
        def remove_wall(self, wall):
            self.walls &= ~wall

        def print_base(
                self,
                stdscr: c.window,
                palette: int,
                horizontal_offset: int,
                vertical_offset: int
                ):
            """Print only the sides of the cell that will not change
            Args:
                stdscr: the curses standard screen
                palette: an int representing the curses color palette
                horizontal_offset: the horizontal offset calculated to print
                    the x axys of the labirinth centered on the stdscr
                vertical_offset: the vertical offset calculated to print
                    the y axys of the labirinth centered on the stdscr

            Returns:
                None 
            """
            row = (self.x * 2) + vertical_offset
            col = (self.y * 4) + horizontal_offset
            if not self.x:
                stdscr.addstr(row, col + 1, '━' * 3, palette)
                if self.y == self.height - 1:
                    stdscr.addch(row, col + 4, '┓', palette)
                else:
                    stdscr.addch(row, col + 4, '┳', palette)
            if not self.y:
                stdscr.addch(row, col, '┣', palette)
                stdscr.addch(row + 1, col, '┃', palette)
                if self.x == 0:
                    stdscr.addch(row, col, '┏', palette)
                elif self.x == self.width - 1: # ultima casella in basso a sx
                    stdscr.addch(row + 2, col, '┗', palette)
            if self.y == self.height - 1:
                stdscr.addch(row + 2, col + 4, '┫', palette)
                stdscr.addch(row + 1, col + 4, '┃', palette)
            if self.y != self.height - 1:
                stdscr.addch(row + 2, col + 4, '╋', palette)
            if self.x == self.width - 1:
                stdscr.addch(row + 2, col + 4, '┻', palette)
                stdscr.addstr(row + 2, col + 1, '━' * 3, palette)
                if self.y == self.height - 1:
                    stdscr.addch(row + 2, col + 4, '┛', palette)

        def print_self(
                self,
                stdscr: c.window,
                palette: int,
                horizontal_offset: int,
                vertical_offset: int
                ):
            """Print walls or spaces if there is no walls.
                    It prints:
                        -right and down of the cell;
                        -up and left if the cell is a border cell
            Args:
                stdscr: the curses standard screen
                palette: an int representing the curses color palette
                horizontal_offset: the horizontal offset calculated to print
                    the x axys of the labirinth centered on the stdscr
                vertical_offset: the vertical offset calculated to print
                    the y axys of the labirinth centered on the stdscr

            Returns:
                None 
            """
            row = (self.x * 2) + vertical_offset
            col = (self.y * 4) + horizontal_offset
            if self.walls.DOWN:
                stdscr.addstr(row + 2, col + 1, '━' * 3, palette)
            if self.walls.RIGHT:
                stdscr.addch(row + 1, col + 4, '┃', palette)
    
    def __init__(
            self,
            width: int,
            height: int,
            ):
        """
        Initialize a maze generator instance

        Args:
            width: width of the labyrinth
            height: height of the labyrinth
            maze: the matrix representation of a labyrinth
        """
        self.maze: list[list[MazeGenerator.Cell]] = [
            [self.Cell(x, y, width, height) for y in range(height)]
            for x in range(width)
        ]
        self.r_seed = seed(1)
        self.width = width
        self.height = height
        
    def __getitem__(self, index):
        """Makes MazeGenerator a subscriptable object.

        Raises:
            IndexError: if the given index is out of range

        Returns:
            self.maze at the required index
        """
        return self.maze[index]


    def get_random_cell(self):
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)
        cell = self[x][y]
        return cell

    def dfs(self):
        cell = get_random_cell()
        cell.is_visited = True
        stack = []
        stack.append(cell)
        while stack:
            current = stack[-1]
            


