from __future__ import annotations
import curses as c
from dataclasses import dataclass, field
from enum import IntFlag
from typing import ClassVar


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


    def opposite_wall(self) -> Wall:
        """Receives a single wall and returns its reversed value"""
        if self == Wall.UP:
            return Wall.DOWN
        if self == Wall.DOWN:
            return Wall.UP
        if self == Wall.LEFT:
            return Wall.RIGHT
        if self == Wall.RIGHT:
            return Wall.LEFT

        raise ValueError(f"Invalid wall: {self}")


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
    walls: "Wall" = field(
            default_factory=lambda: Wall(0xF)
            )
    is_visited: bool = False
    ft_logo: bool = False
    entry: bool = False
    end: bool = False
    explored: bool = False
    is_path: bool = False
    parent: Cell | None = None
    mouse_tracks: ClassVar[int] = 0
    direction: str = ""

    def adjacent_cell(self, wall: str) -> tuple[
                            int, int]:
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
        raise ValueError(f"Invalid wall: {wall}")


    def remove_wall(self, wall: "Wall") -> None:
        self.walls &= ~wall

    def print_base(
            self,
            stdscr: c.window,
            palette: int,
            horizontal_offset: int,
            vertical_offset: int
            ) -> None:
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
            vertical_offset: int,
            ) -> None:
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
        stdscr.addstr(
            row + 2,
            col + 1,
            '━' * 3 if self.walls & Wall.DOWN else '   ',
            palette
        )
        stdscr.addch(
            row + 1,
            col + 4,
            '┃' if self.walls & Wall.RIGHT else ' ',
            palette
        )
        if self.ft_logo:
            stdscr.addstr(row + 1, col + 1, 'X' * 3, palette)
        elif self.entry:
            stdscr.addch(row + 1, col + 1, '🐭', palette)
        elif self.end:
            stdscr.addch(row + 1, col + 1, '🧀', palette)
        elif self.is_path:
            type(self).mouse_tracks += 1
            if type(self).mouse_tracks % 3:
                stdscr.addstr(row + 1, col + 1, ' * ', palette)
            else:
                stdscr.addstr(row + 1, col + 2, '* ', palette)
