from typing import Iterator, cast
from .logos import LOGO_42
from .cell import Cell, Wall
from .algorithms_utils import (
        _random_valid_starting_cell,
        _valid_walls,
        _print_animation,
        _valid_closest_cells,
        open_walls,
        closed_valid_walls,
        remove_dead_ends,
        restore_walls,
        coordinates_to_cell,
        give_direction
        )
from .algorithms import prim_algorithm, dfs, bfs

ConfigValue = str | int | bool | tuple[int, int] | float
Configs = dict[str, ConfigValue]


class MazeGenerator:
    """Represents the Maze and offers tools to work with it.

    Attributes:
        conf: The maze configuration
        width: The number of maze rows
        height: The number of maze columns.
        entry: The entry coordinates.
        exit: The exit coordinates
        maze: The matrix of maze cells.
        ft_logo: The coordinates of the 42 logo.
        removed_walls: The walls removed in non-perfect mode
        generated: Wheter the maze has been generated
        path: The curreny solution path
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
        self.width = cast(int, configs["WIDTH"])
        self.height = cast(int, configs["HEIGHT"])
        self.entry = cast(tuple[int, int], configs["ENTRY"])
        self.exit = cast(tuple[int, int], configs["EXIT"])
        self.removed_walls: list[tuple[Cell, Wall]] = []
        self.generated_path: bool = False
        self.generated: bool = False
        self.path: str = ""
        self.ft_logo: list[tuple[int, int]] = self._logo_offset(LOGO_42)
        self.maze: list[list[Cell]] = []
        self._fill_maze()
        self._error_if_entry_exit_in_logo()

    def _fill_maze(self) -> None:
        """
        Fill the maze with cell

        Args:
            A MazeGenerator instance.

        Raises:
            AssertionError: if the maze is too small to exist.

        Returns:
            None
        """
        cell_counter: int = 0
        for x in range(self.width):
            rows: list[Cell] = []
            for y in range(self.height):
                cell_params = (x, y, self.width, self.height)
                for ft_x, ft_y in self.ft_logo:
                    if (
                        ft_x == x and ft_y == y and
                        self.width >= 5 and self.height >= 7
                    ):
                        rows.append(self.Cell(*cell_params, ft_logo=True))
                        break
                else:
                    rows.append(self.Cell(*cell_params, ft_logo=False))
                cell_counter += 1
            self.maze.append(rows)
        assert cell_counter >= 2

    def _logo_offset(
            self, logo: tuple[tuple[int, int], ...]
                     ) -> list[tuple[int, int]]:
        """
        Apply an offset to a deepcopy of the  logo to center it in the maze.

        Args:
            self: the MazeGenerator instance.
            logo: the logo to print inside the maze.

        Returns:
            A deepcopy of the received logo moved by horizontal and
            vertical offset
        """
        horizontal_offset = (self.width - 5) // 2
        vertical_offset = (self.height - 7) // 2
        return [
                (x + horizontal_offset, y + vertical_offset)
                for x, y in logo
                ]

    def _error_if_entry_exit_in_logo(self) -> None:
        """
        Raises an error if entry or exit is inside the maze logo.

        Args:
            A MazeGenerator instance.

        Raises:
            ValueError if exit or entry is inside the maze logo.

        Returns:
            None
        """
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

    _random_valid_starting_cell = _random_valid_starting_cell
    _valid_walls = _valid_walls
    _print_animation = _print_animation
    _valid_closest_cells = _valid_closest_cells
    open_walls = open_walls
    closed_valid_walls = closed_valid_walls
    remove_dead_ends = remove_dead_ends
    restore_walls = restore_walls
    coordinates_to_cell = coordinates_to_cell
    give_direction = give_direction
    prim_algorithm = prim_algorithm
    dfs = dfs
    bfs = bfs
