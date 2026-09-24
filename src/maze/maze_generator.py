import curses as c
from time import sleep
from enum import IntFlag
from dataclasses import dataclass, field
from itertools import product
from typing import Callable

class MazeGenerator:
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
        LEFT = 2 # 0010
        DOWN = 4 # 0100
        RIGHT = 8 # 1000

    @dataclass
    class Cell:
        x: int
        y: int
        width: int
        height: int
        walls: MazeGenerator.Wall = field(
                default_factory=lambda: MazeGenerator.Wall(0xF)
                )
        is_visited: bool = False
        entry: bool = False
        end: bool = False

        def print_base(
                self,
                stdscr: c.window,
                palette: int,
                horizontal_offset: int,
                vertical_offset: int
                ):
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
            "Prints walls. It prints right and down, up and left only if you're on the border cells'"
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
        self.maze: list[list[MazeGenerator.Cell]] = [
                                    [
                                    self.Cell(
                                        x,
                                        y,
                                        width,
                                        height,
                                        ) for y in range(height)
                                    ] for x in range(width)
                                    ]
