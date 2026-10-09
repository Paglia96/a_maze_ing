from time import sleep
from random import seed, choice, randint
from .cell import Cell, Wall


class MazeGenerator:
    """Represents the Maze and offers tools to work with it.

    Attributes:
        width: width of the labyrinth
        height: height of the labirinth
        maze: the labirinth
    """

    Cell = Cell
    Wall = Wall

    def __init__(self, configs: dict):
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
        self.conf = configs
        self.ft_logo: tuple[list[str]] = (
            [0, 0],
            [1, 0],
            [2, 0],
            [2, 1],
            [2, 2],
            [3, 2],
            [4, 2],
            [0, 4],
            [0, 5],
            [0, 6],
            [1, 6],
            [2, 4],
            [2, 5],
            [2, 6],
            [3, 4],
            [4, 4],
            [4, 5],
            [4, 6],
        )
        for cell in self.ft_logo:
            cell[0] += (horizontal_offset := (configs["WIDTH"] - 5) // 2)
            cell[1] += (vertical_offset := (configs["HEIGHT"] - 7) // 2)

        self.maze: list[list[MazeGenerator.Cell]] = []
        for x in range(configs["WIDTH"]):
            rows: list[MazeGenerator.Cell] = []
            for y in range(configs["HEIGHT"]):
                for ft_x, ft_y in self.ft_logo:
                    if (
                        ft_x == x
                        and ft_y == y
                        and configs["WIDTH"] >= 5
                        and configs["HEIGHT"] >= 7
                    ):
                        rows.append(
                            self.Cell(
                                x, y, configs["WIDTH"], configs["HEIGHT"], ft_logo=True
                            )
                        )
                        break
                else:
                    rows.append(
                        self.Cell(
                            x, y, configs["WIDTH"], configs["HEIGHT"], ft_logo=False
                        )
                    )
            self.maze.append(rows)
        for x, y in (configs["ENTRY"], configs["EXIT"]):
            if self.maze[x][y].ft_logo:
                raise ValueError(
                    "Entry and exit can't be inside the maze logo\n"
                    "Please, choose other values for them"
                )

    def __getitem__(self, index):
        """Makes MazeGenerator a subscriptable object.

        Raises:
            IndexError: if the given index is out of range

        Returns:
            self.maze at the required index
        """
        return self.maze[index]

    def _random_valid_starting_cell(self):
        while (
            cell := self[randint(0, self.conf["WIDTH"] - 1)][
                randint(0, self.conf["HEIGHT"] - 1)
            ]
        ).ft_logo:
            pass
        return cell

    def _valid_walls(self, cell):
        """Receives a cell and returns a list of walls considered valid
        The wall of a cell is considered valid if:
        -the adjacent cell is still not visited
        -the wall is breakable (not an edge of the maze, not part of the 42 logo)
        """
        walls = [wall for wall in cell.walls]
        valid_walls = []
        for wall in walls:
            if cell.x == 0:
                if (
                    wall.name == "UP"
                    or (cell.y == 0 and wall.name == "LEFT")
                    or (cell.y == self.conf["HEIGHT"] - 1 and wall.name == "RIGHT")
                ):
                    continue
            if cell.x == self.conf["WIDTH"] - 1:
                if (
                    wall.name == "DOWN"
                    or (cell.y == 0 and wall.name == "LEFT")
                    or (cell.y == self.conf["HEIGHT"] - 1)
                    and wall.name == "RIGHT"
                ):
                    continue
            if (cell.y == 0 and wall.name == "LEFT") or (
                cell.y == self.conf["HEIGHT"] - 1 and wall.name == "RIGHT"
            ):
                continue
            cell2 = self[(i := cell.adjacent_cell(wall.name))[0]][i[1]]
            if cell2.ft_logo is True:
                continue
            if not cell2.is_visited:
                valid_walls.append(wall)
        return valid_walls

    def _print_animation(
        self,
        current,
        adjacent,
        stdscr,
        palette,
        horizontal_offset,
        vertical_offset,
        seconds,
    ):
        current.print_self(stdscr, palette, horizontal_offset, vertical_offset)
        adjacent.print_self(stdscr, palette, horizontal_offset, vertical_offset)
        stdscr.refresh()
        sleep(seconds / (self.conf["HEIGHT"] * self.conf["WIDTH"]))

    def prim_algorithm(
        self,
        stdscr: c.window,
        palette: int,
        horizontal_offset: int,
        vertical_offset: int,
        seed_rand: int,
        seconds: float,
    ):
        seed(seed_rand)
        cells: list = [self._random_valid_starting_cell()]
        cells[0].is_visited = True
        while cells:
            current = choice(cells)
            try:
                wall = choice(self._valid_walls(current))
            except IndexError:  # choice riceve lista vuota
                cells.remove(current)
                continue
            adjacent = self[(xy := current.adjacent_cell(wall.name))[0]][xy[1]]
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

    def _valid_closest_cells(self, cell):
        closest_cells = []
        for wall in self._valid_walls(cell):
            x, y = cell.adjacent_cell(wall.name)
            adjacent = self[x][y]
            closest_cells.append((adjacent, wall))
        return closest_cells

    def dfs(
        self,
        stdscr: c.window,
        palette: int,
        horizontal_offset: int,
        vertical_offset: int,
        seed_rand: int,
        seconds: float,
    ):
        seed(seed_rand)
        stack: list = [self._random_valid_starting_cell()]
        stack[0].is_visited = True
        while stack:
            current = stack.pop()
            closest: tuple = self._valid_closest_cells(current)
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

    def open_walls(self, cell) -> int:
        "Counts the open walls of a cell"
        "if has only one wall open is a dead end"
        count = 0
        for wall in self.Wall:
            if not (cell.walls & wall):
                count += 1
        return count

    def closed_valid_walls(
        self, cell
    ) -> list[tuple["MazeGenerator.Wall", "MazeGenerator.Cell"]]:
        "same of valid walls but controls"
        "only if the wall is breakable (no border no logo)"

        breakable_walls = []

        for wall in self.Wall:
            if not (cell.walls & wall):
                continue
            xy = cell.adjacent_cell(wall.name)
            if not (
                0 <= xy[0] < self.conf["WIDTH"] and 0 <= xy[1] < self.conf["HEIGHT"]
            ):
                continue
            adjacent = self[xy[0]][xy[1]]
            if adjacent.ft_logo:
                continue
            breakable_walls.append((wall, adjacent))

        return breakable_walls

    def remove_dead_ends(
        self,
        stdscr: c.window,
        palette: int,
        horizontal_offset: int,
        vertical_offset: int,
        seconds: int,
    ) -> None:

        while True:
            dead_ends = []

            for row in self.maze:
                for cell in row:
                    if cell.ft_logo:
                        continue
                    if self.open_walls(cell) == 1:
                        dead_ends.append(cell)
            if not dead_ends:
                break

            changed = False

            for cell in dead_ends:
                if self.open_walls(cell) != 1:
                    continue
                breakable_walls = self.closed_valid_walls(cell)
                if not breakable_walls:
                    continue
                wall, adjacent = choice(breakable_walls)
                cell.remove_wall(wall)
                adjacent.remove_wall(wall.opposite_wall())
                self._print_animation(
                    cell,
                    adjacent,
                    stdscr,
                    palette,
                    horizontal_offset,
                    vertical_offset,
                    seconds,
                )

                changed = True

            if not changed:
                break

    def coordinates_to_cell(self, config_cell: tuple, node_type: str):
        cell = self[config_cell[0]][config_cell[1]]
        cell.entry = node_type == "Entry"
        cell.end = node_type == "Exit"
        return cell

    def bfs(self, stdscr: c.window) -> None:
        """Finds the shortest path usign breadth first search alghorithm,
        storing each cell parent and rebuilding the path from exit to entry
        """
        from collections import deque
        from itertools import chain

        # resetta a ogni chiamata
        for cell in chain.from_iterable(self.maze):
            cell.explored = False
            cell.parent = None
            cell.is_path = False
            cell.entry = False
            cell.end = False

        entry_cell = self.coordinates_to_cell(self.conf["ENTRY"], "Entry")
        exit_cell = self.coordinates_to_cell(self.conf["EXIT"], "Exit")
        for cell in (entry_cell, exit_cell):
            cell.print_self(
                stdscr,
                self.conf["PALETTE"],
                self.conf["HORIZONTAL_OFFSET"],
                self.conf["VERTICAL_OFFSET"],
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
                    x, y = current.adjacent_cell(wall.name)
                    adjacent = self[x][y]
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
                    self.conf["PALETTE"],
                    self.conf["HORIZONTAL_OFFSET"],
                    self.conf["VERTICAL_OFFSET"],
                )
                stdscr.refresh()
                sleep(self.conf["SECONDS"] / (self.conf["WIDTH"] * self.conf["HEIGHT"]))

                if curr == entry_cell:
                    break
                curr = curr.parent
