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
        ft_logo: bool = False

        entry: bool = False
        end: bool = False

        explored: bool = False
        is_path: bool = False
        parent: "MazeGenerator.Cell" = None

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
                vertical_offset: int,
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
            stdscr.addstr(
                row + 2,
                col + 1,
                '━' * 3 if self.walls & MazeGenerator.Wall.DOWN else '   ',
                palette
            )
            stdscr.addch(
                row + 1,
                col + 4,
                '┃' if self.walls & MazeGenerator.Wall.RIGHT else ' ',
                palette
            )
            if self.ft_logo:
                stdscr.addstr(row + 1, col + 1, 'X' * 3, palette)
            elif self.entry:
                stdscr.addstr(row + 1, col + 1, '🐭', palette)
            elif self.end:
                stdscr.addstr(row + 1, col + 1, '🧀', palette)
            elif self.is_path:
                stdscr.addstr(row + 1, col + 1, 'o' * 3, palette)

    
    def __init__(
            self,
            width: int,
            height: int
            ):
        """
        Initialize a maze generator instance

        Args:
            width: width of the labyrinth
            height: height of the labyrinth
            maze: the matrix representation of a labyrinth
        """
        """
        Maze minimum width 8 min height 6
        to find horizontal_offset= (maze_width - ft_width) /2
        vertical_offset= (maze_height - ft_height) /2
        Logo width x height 7 x 4
        
        """
        self.__horizontal_offset: int = (width - 5) // 2
        self.__vertical_offset: int = (height - 7) // 2
        
        self.ft_logo = [
            [0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [3, 2], [4, 2],
            [0, 4], [0, 5], [0, 6], [1, 6], [2, 4], [2, 5],
            [2, 6], [3, 4], [4, 4], [4, 5], [4, 6]
        ]

        for cell in self.ft_logo:
            cell[0] += self.__horizontal_offset
            cell[1] += self.__vertical_offset

        self.maze: list[list[MazeGenerator.Cell]] = []

        for x in range(width):
            rows: list[MazeGenerator.Cell] = []
            for y in range(height):
                for ft_x, ft_y in self.ft_logo:
                    if ft_x == x and ft_y == y:
                        rows.append(self.Cell(x, y, width, height, ft_logo=True))
                        break
                else:
                    rows.append(self.Cell(x, y, width, height, ft_logo=False))
            self.maze.append(rows)


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
    
    def __random_valid_starting_cell(self):
        while (cell := self[
            randint(0, self.width - 1)
        ][
            randint(0, self.height - 1)
        ]).ft_logo:
            pass
        return cell
    
    def __valid_walls(self, cell):
        """Receives a cell and returns a list of walls considered valid
        The wall of a cell is considered valid if:
        -the adjacent cell is still not visited
        -the wall is breakable (not an edge of the maze, not part of the 42 logo)
        """
        walls = [wall for wall in cell.walls]
        valid_walls = []
        for wall in walls:
            if cell.x == 0:
                if wall.name == 'UP' or (cell.y == 0 and wall.name == 'LEFT') or (cell.y == self.height - 1 and wall.name == 'RIGHT'):
                    continue
            if cell.x == self.width - 1:
                if wall.name == 'DOWN' or (cell.y == 0 and wall.name == 'LEFT') or (cell.y == self.height - 1) and wall.name == 'RIGHT':
                    continue
            if (cell.y == 0 and wall.name == 'LEFT') or (cell.y == self.height - 1 and wall.name == 'RIGHT'):
                continue
            cell2 = self[(i := cell.adjacent_cell(wall.name))[0]][i[1]]
            if cell2.ft_logo is True:
                continue
            if not cell2.is_visited:
                valid_walls.append(wall)
        return valid_walls

    def __print_animation(
            self,
            current,
            adjacent,
            stdscr,
            palette,
            horizontal_offset,
            vertical_offset,
            seconds
            ):
        current.print_self(stdscr, palette, horizontal_offset, vertical_offset)
        adjacent.print_self(stdscr, palette, horizontal_offset, vertical_offset)
        stdscr.refresh()
        sleep(seconds / (self.height * self.width))

    def prim_algorithm(
                self,
                stdscr: c.window,
                palette: int,
                horizontal_offset: int,
                vertical_offset: int,
                seed_rand: int,
                seconds: float
                ):
        seed(seed_rand)
        cells: list = [self.__random_valid_starting_cell()]
        cells[0].is_visited = True
        while cells:
            current = choice(cells)
            try:
                wall = choice(self.__valid_walls(current))
            except IndexError: # choice riceve lista vuota
                cells.remove(current)
                continue
            adjacent = self[(i := current.adjacent_cell(wall.name))[0]][i[1]]
            adjacent.is_visited = True
            cells.append(adjacent)
            wall2 = wall.opposite_wall()
            current.remove_wall(wall)
            adjacent.remove_wall(wall2)
            self.__print_animation(current, adjacent, stdscr, palette, horizontal_offset, vertical_offset, seconds)


    def __valid_closest_cells(self, cell):
        closest_cells = []
        for wall in self.__valid_walls(cell):
            xy = cell.adjacent_cell(wall.name)
            cell2 = self[xy[0]][xy[1]]
            closest_cells.append((cell2, wall))
        return closest_cells

    def dfs(self, stdscr: c.window,
                palette: int,
                horizontal_offset: int,
                vertical_offset: int,
                seed_rand: int,
                seconds: float
                ):
        seed(seed_rand)
        cell = self.__random_valid_starting_cell()
        cell.is_visited = True
        stack = []
        stack.append(cell)
        while stack:
            current = stack.pop()
            closest = self.__valid_closest_cells(current)
            if closest:
                stack.append(current)
                adjacent, wall = choice(closest)
                current.remove_wall(wall)
                adjacent.remove_wall(wall.opposite_wall())
                adjacent.is_visited = True
                stack.append(adjacent)
                self.__print_animation(current, adjacent, stdscr, palette, horizontal_offset, vertical_offset, seconds)


    def cell_coordinates_given(self, config_cell: tuple):
        cell = self[config_cell[0]][config_cell[1]]
        return cell

    def bfs(self, stdscr: c.window,
                palette: int,
                horizontal_offset: int,
                vertical_offset: int,
                seconds: float,
                configs: dict
                ) -> None:
    
        from collections import deque
        
        # resetta a ogni chiamata
        for row in self.maze:
            for cell in row:
                cell.explored = False
                cell.parent = None
                cell.is_path = False
                cell.entry = False
                cell.end = False

        entry_cell = self.cell_coordinates_given(configs['ENTRY'])
        #if entry not in logo
        entry_cell.entry = True
        exit_cell = self.cell_coordinates_given(configs['EXIT'])
        # If exit cell not in logo to add
        exit_cell.end = True

        for row in self.maze:
            for cell in row:
                cell.print_self(
                    stdscr,
                    palette,
                    horizontal_offset,
                    vertical_offset
                )
        stdscr.refresh()

        exploring = deque([entry_cell])
        entry_cell.explored = True
        found_exit = False
        while exploring and not found_exit:
            current = exploring.popleft()
            if current == exit_cell:
                found_exit = True
                break

            for wall in self.Wall:
                if not (current.walls & wall):
                    xy = current.adjacent_cell(wall.name)
                    adjacent = self[xy[0]][xy[1]]
                    if not adjacent.explored:
                        adjacent.explored = True
                        adjacent.parent = current
                        exploring.append(adjacent)

        if found_exit:
            curr = exit_cell
            while curr:
                curr.is_path = True

                curr.print_self(
                    stdscr,
                    palette,
                    horizontal_offset,
                    vertical_offset
                )
                stdscr.refresh()
                sleep(seconds / (self.width * self.height))

                if curr == entry_cell:
                    break
                # qui devo printare il percorso nella cella
                curr = curr.parent
