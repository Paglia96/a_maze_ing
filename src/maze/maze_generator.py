from time import sleep
from typing import Callable, ClassVar, Iterator
from random import seed, choice, randint
from ..parser import Configs
from .cell import Wall, Cell
from typing import cast
import curses as c


class MazeGenerator:
    """Represents the Maze and offers tools to work with it.

    Attributes:
        width: width of the labyrinth
        height: height of the labirinth
        maze: the labirinth
    """

    from .cell import Wall, Cell
    
    def __init__(self, configs: Configs) -> None:
        """
        Initialize a maze generator instance

        Args:
            configs: The maze configuration
        
        Raises:
            ValueError: If the entry or exit is inside the logo
        """
        self.conf = configs
        self.width = cast(int, configs['WIDTH'])
        self.height = cast(int, configs['HEIGHT'])
        self.entry = cast(tuple[int, int], configs['ENTRY'])
        self.exit = cast(tuple[int, int], configs['EXIT'])
        self.removed_walls: list[tuple[Cell, Wall]] = []
        self.generated_path: bool = False
        self.ft_logo = (
            [0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [3, 2], [4, 2],
            [0, 4], [0, 5], [0, 6], [1, 6], [2, 4], [2, 5],
            [2, 6], [3, 4], [4, 4], [4, 5], [4, 6]
            )
        for cell in self.ft_logo:
            cell[0] += (
                horizontal_offset := (self.width - 5) // 2
            )
            cell[1] += (
                vertical_offset := (self.height - 7) // 2
                )

        self.maze: list[list[Cell]] = []
        for x in range(self.width):
            rows: list[Cell] = []
            for y in range(self.height):
                for ft_x, ft_y in self.ft_logo:
                    if (ft_x == x and ft_y == y
                        and self.width >= 5 and
                            self.height >= 7):
                        rows.append(self.Cell(
                            x, y, self.width, self.height,
                            ft_logo=True
                            ))
                        break
                else:
                    rows.append(self.Cell(
                        x, y, self.width, self.height,
                        ft_logo=False
                        ))
            self.maze.append(rows)
        for x, y in (self.entry, self.exit):
            if self.maze[x][y].ft_logo:
                raise ValueError(
                        "Entry and exit can't be inside the maze logo\n"
                        "Please, choose other values for them"
                        )

        
    def __getitem__(self, index: int) -> list[Cell]:
        """Return the cells at the given index.

        Args:
            index: The requested index.

        Returns:
            A list of cells.
        """
        return self.maze[index]

    def __iter__(self) -> Iterator[list[Cell]]:
        """Return an iterator over the maze.

        Returns:
            An iterator over the maze columns.
        """
        return iter(self.maze)


    def get_maze(self) -> list[list[Cell]]:
        """Return the maze matrix.

        Returns:
            The matrix of cells.
        """
        return self.maze
    
    def _random_valid_starting_cell(self) -> Cell:
        """Choose a random cell outside the logo.

        Returns:
            A valid starting cell.
        """
        while (cell := self[
            randint(0, self.width - 1)
        ][
            randint(0, self.height - 1)
        ]).ft_logo:
            pass
        return cell


    def _valid_walls(
            self, cell: Cell
            ) -> list[Wall]:
        """Find closed walls leading to unvisited cells.

            Args:
            cell: The cell to check.

            Returns:
                A list of valid walls.
        """
        walls = [wall for wall in self.Wall if cell.walls & wall]
        valid_walls = []
        for wall in walls:
            if cell.x == 0:
                if wall.name == 'UP' or (
                    cell.y == 0 and wall.name == 'LEFT'
                    ) or (cell.y == self.height - 1 and wall.name == 'RIGHT'):
                    continue
            if cell.x == self.width - 1:
                if wall.name == 'DOWN' or (
                    cell.y == 0 and wall.name == 'LEFT'
                    ) or (cell.y == self.height - 1) and wall.name == 'RIGHT':
                    continue
            if (
                cell.y == 0 and wall.name == 'LEFT'
                ) or (cell.y == self.height - 1 and wall.name == 'RIGHT'):
                continue
            cell2 = self[
                (i := cell.adjacent_cell(cast(str, wall.name)))[0]
                 ][i[1]]
            if cell2.ft_logo is True:
                continue
            if not cell2.is_visited:
                valid_walls.append(wall)
        return valid_walls


    def _print_animation(
            self,
            current: Cell,
            adjacent: Cell,
            stdscr: c.window,
            palette: int,
            horizontal_offset: int,
            vertical_offset: int,
            seconds: float
            ) -> None:
        """Draw two cells and refresh the screen.

        Args:
            current: The current cell.
            adjacent: The adjacent cell.
            stdscr: The curses window.
            palette: The color palette.
            horizontal_offset: The horizontal screen offset.
            vertical_offset: The vertical screen offset.
            seconds: The animation duration.
        """
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
                ) -> None:
        """Generate a maze using Prim's algorithm.

        Args:
            stdscr: The curses window.
            palette: The color palette.
            horizontal_offset: The horizontal screen offset.
            vertical_offset: The vertical screen offset.
            seed_rand: The random seed.
            seconds: The animation duration.
        """
        seed(seed_rand)
        cells: list[Cell] = [
            self._random_valid_starting_cell()
            ]
        cells[0].is_visited = True
        while cells:
            current = choice(cells)
            try:
                wall = choice(self._valid_walls(current))
            except IndexError:  # choice riceve lista vuota
                cells.remove(current)
                continue
            adjacent = self[
                (xy := current.adjacent_cell(cast(str, wall.name)))[0]
                ][xy[1]]
            adjacent.is_visited = True
            cells.append(adjacent)
            wall2 = wall.opposite_wall()
            current.remove_wall(wall)
            adjacent.remove_wall(wall2)
            self._print_animation(
                current,
                adjacent,
                stdscr,
                palette,
                horizontal_offset,
                vertical_offset,
                seconds,
            )


    def _valid_closest_cells(
            self, cell: Cell
            ) -> list[tuple[Cell, Wall]]:
        """Generate a maze using DFS.

        Args:
            stdscr: The curses window.
            palette: The color palette.
            horizontal_offset: The horizontal screen offset.
            vertical_offset: The vertical screen offset.
            seed_rand: The random seed.
            seconds: The animation duration.
        """
        closest_cells = []
        for wall in self._valid_walls(cell):
            x, y = cell.adjacent_cell(cast(str, wall.name))
            adjacent = self[x][y]
            closest_cells.append((adjacent, wall))
        return closest_cells


    def dfs(self, stdscr: c.window,
                palette: int,
                horizontal_offset: int,
                vertical_offset: int,
                seed_rand: int,
                seconds: float
                ) -> None:
        """Generate a maze using DFS.

        Args:
            stdscr: The curses window.
            palette: The color palette.
            horizontal_offset: The horizontal screen offset.
            vertical_offset: The vertical screen offset.
            seed_rand: The random seed.
            seconds: The animation duration.
        """
        seed(seed_rand)
        stack: list[Cell] = [
            self._random_valid_starting_cell()
            ]
        stack[0].is_visited = True
        while stack:
            current = stack.pop()
            closest: list[
                tuple[Cell, Wall]
                ] = self._valid_closest_cells(current)
            if closest:
                stack.append(current)
                adjacent, wall = choice(closest)
                current.remove_wall(wall)
                adjacent.remove_wall(wall.opposite_wall())
                adjacent.is_visited = True
                stack.append(adjacent)
                self._print_animation(
                    current,
                    adjacent,
                    stdscr,
                    palette,
                    horizontal_offset,
                    vertical_offset,
                    seconds,
                )


    def open_walls(self, cell: Cell) -> int:
        """Count the open walls of a cell.

        Args:
            cell: The cell to check.

        Returns:
            The number of open walls.
        """
        count = 0
        for wall in self.Wall:
            if not (cell.walls & wall):
                count += 1
        return count


    def closed_valid_walls(
            self, cell: Cell
            ) -> list[tuple[Wall, Cell]]:
        """Find breakable walls and their neighboring cells.

        Args:
            cell: The cell to check.

        Returns:
            A list of walls and their neighboring cells.
        """

        breakable_walls = []

        for wall in self.Wall:
            if not (cell.walls & wall):
                continue
            xy = cell.adjacent_cell(cast(str, wall.name))
            if not(
                0 <= xy[0] < self.width
                and 0 <= xy[1] < self.height
            ):
                continue
            adjacent = self[xy[0]][xy[1]]
            if adjacent.ft_logo:
                continue
            breakable_walls.append((wall, adjacent))

        return breakable_walls


    def remove_dead_ends(
            self,
            stdscr:c.window,
            palette: int,
            horizontal_offset: int,
            vertical_offset: int,
            seconds: float
            ) -> None:
        """Remove dead ends by opening extra walls.

        Args:
            stdscr: The curses window.
            palette: The color palette.
            horizontal_offset: The horizontal screen offset.
            vertical_offset: The vertical screen offset.
            seconds: The animation duration.
        """

        dead_ends = []

        for row in self.maze:
            for cell in row:
                if cell.ft_logo:
                    continue
                if self.open_walls(cell) == 1:
                    dead_ends.append(cell)

        for cell in dead_ends:
            if self.open_walls(cell) != 1:
                continue
            breakable_walls = self.closed_valid_walls(cell)
            if not breakable_walls:
                continue
            wall, adjacent = choice(breakable_walls)
            cell.remove_wall(wall)
            self.removed_walls.append((cell, wall))
            adjacent.remove_wall(wall.opposite_wall())
            self.removed_walls.append((adjacent, wall.opposite_wall()))
            self._print_animation(
                            cell,
                            adjacent,
                            stdscr,
                            palette,
                            horizontal_offset,
                            vertical_offset,
                            seconds
                            )


    def restore_walls(
            self,
            stdscr: c.window,
            palette: int,
            horizontal_offset: int,
            vertical_offset: int,
            seconds: float
            ) -> None:
        while self.removed_walls:
            cell, wall = self.removed_walls.pop()
            cell.add_wall(wall)
            cell.print_self(
                            stdscr,
                            palette,
                            horizontal_offset,
                            vertical_offset,
                            )
            stdscr.refresh()
            sleep(seconds / (self.height * self.width))


    def coordinates_to_cell(
            self, config_cell: tuple[int, int], node_type: str
            ) -> Cell:
        """Get a cell and mark it as entry or exit.

        Args:
            config_cell: The cell coordinates.
            node_type: The type of cell.

        Returns:
            The updated cell.
        """
        cell: MazeGenerator.Cell = self[config_cell[0]][config_cell[1]]
        cell.entry = node_type == "Entry"
        cell.end = node_type == "Exit"
        return cell


    def give_direction(self, wall_name: str) -> str:
        """Convert a wall name into a direction.

        Args:
            wall_name: The name of the wall.

        Returns:
            The cardinal direction.

        Raises:
            ValueError: If the wall name is invalid.
        """
        match wall_name:
            case "DOWN":
                return "S"
            case "UP":
                return "N"
            case "RIGHT":
                return "E"
            case "LEFT":
                return "W"
            case _:
                raise ValueError(f"Invalid wall name:{wall_name}")


    def bfs(self, stdscr: c.window) -> str:
        """Find the shortest path using BFS.

        Args:
            stdscr: The curses window.

        Returns:
            The path directions, or an empty string if no path exists.
        """
        from collections import deque
        from itertools import chain

        # resetta a ogni chiamata
        for row in self.maze:
            for cell in row:
                cell.explored = False
                cell.parent = None
                cell.is_path = False
                cell.entry = False
                cell.end = False
        
        palette = cast(int, self.conf['PALETTE'])
        horizontal_offset = cast(int, self.conf['HORIZONTAL_OFFSET'])
        vertical_offset = cast(int, self.conf['VERTICAL_OFFSET'])
        seconds = cast(float, self.conf['SECONDS'])

        entry_cell = self.coordinates_to_cell(self.entry, 'Entry')
        exit_cell = self.coordinates_to_cell(self.exit, 'Exit')
        for row in self.maze:
            for cell in row:
                cell.print_self(
                    stdscr, palette, horizontal_offset,
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
                    if wall.name is None:
                        continue
                    x, y = current.adjacent_cell(cast(str, wall.name))
                    adjacent = self[x][y]
                    if not adjacent.explored:
                        adjacent.explored = True
                        adjacent.parent = current
                        adjacent.direction = self.give_direction(wall.name)
                        exploring.append(adjacent)

        if found_exit:
            curr: Cell | None = exit_cell
            path: list[str] = []
            while curr:
                curr.is_path = True
                path.append(curr.direction)
                curr.print_self(
                    stdscr, palette,
                    horizontal_offset, vertical_offset
                )
                stdscr.refresh()
                sleep(seconds / (self.width * self.height))

                if curr == entry_cell:
                    break
                curr = curr.parent
        
        if not exploring and not found_exit:
            return ""
        path.reverse()
        return "".join(path)
