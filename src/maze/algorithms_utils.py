from .cell import Wall, Cell
from random import choice, randint
from time import sleep
from typing import cast, TYPE_CHECKING
import curses as c

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


def _random_valid_starting_cell(self: "MazeGenerator") -> Cell:
    """Choose a random cell outside the logo.

    Returns:
        A valid starting cell.
    """
    x, y = (randint(0, self.width - 1), randint(0, self.height - 1))
    while (cell := self[x][y]).ft_logo:
        x, y = (randint(0, self.width - 1), randint(0, self.height - 1))
    return cell


def _valid_walls(self: "MazeGenerator", cell: Cell) -> list[Wall]:
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
            if (
                wall.name == "UP"
                or (cell.y == 0 and wall.name == "LEFT")
                or (cell.y == self.height - 1 and wall.name == "RIGHT")
            ):
                continue
        if cell.x == self.width - 1:
            if (
                wall.name == "DOWN"
                or (cell.y == 0 and wall.name == "LEFT")
                or (cell.y == self.height - 1)
                and wall.name == "RIGHT"
            ):
                continue
        if (cell.y == 0 and wall.name == "LEFT") or (
            cell.y == self.height - 1 and wall.name == "RIGHT"
        ):
            continue
        x, y = cell.adjacent_cell(cast(str, wall.name))
        cell2 = self[x][y]
        if cell2.ft_logo is True:
            continue
        if not cell2.is_visited:
            valid_walls.append(wall)
    return valid_walls


def _print_animation(
    self: "MazeGenerator",
    current: Cell,
    adjacent: Cell,
    stdscr: c.window,
    palette: int,
    horizontal_offset: int,
    vertical_offset: int,
    seconds: float,
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
    param = (stdscr, palette, horizontal_offset, vertical_offset)
    current.print_self(*param)
    adjacent.print_self(*param)
    stdscr.refresh()
    sleep(seconds / (self.height * self.width))


def _valid_closest_cells(
        self: "MazeGenerator", cell: Cell
) -> list[tuple[Cell, Wall]]:
    """Find valid neighboring cells and their walls.

    Args:
        cell: The cell to check.

    Returns:
        A list of neighboring cells and their walls.
    """
    closest_cells = []
    for wall in self._valid_walls(cell):
        x, y = cell.adjacent_cell(cast(str, wall.name))
        adjacent = self[x][y]
        closest_cells.append((adjacent, wall))
    return closest_cells


def open_walls(self: "MazeGenerator", cell: Cell) -> int:
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
        self: "MazeGenerator", cell: Cell
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
        if not (0 <= xy[0] < self.width and 0 <= xy[1] < self.height):
            continue
        adjacent = self[xy[0]][xy[1]]
        if adjacent.ft_logo:
            continue
        breakable_walls.append((wall, adjacent))

    return breakable_walls


def remove_dead_ends(
    self: "MazeGenerator",
    stdscr: c.window,
    palette: int,
    horizontal_offset: int,
    vertical_offset: int,
    seconds: float,
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
            seconds,
        )


def restore_walls(
    self: "MazeGenerator",
    stdscr: c.window,
    palette: int,
    horizontal_offset: int,
    vertical_offset: int,
    seconds: float,
) -> None:
    """Restore the walls removed in non-perfect mode.

    Args:
        stdscr: The curses window.
        palette: The color palette.
        horizontal_offset: The horizontal screen offset.
        vertical_offset: The vertical screen offset.
        seconds: The animation duration.
    """
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
        self: "MazeGenerator",
        config_cell: tuple[int, int],
        node_type: str
        ) -> Cell:
    """Get a cell and mark it as entry or exit.

    Args:
        config_cell: The cell coordinates.
        node_type: The type of cell.

    Returns:
        The updated cell.
    """
    cell: Cell = self[config_cell[0]][config_cell[1]]
    cell.entry = node_type == "Entry"
    cell.end = node_type == "Exit"
    return cell


def give_direction(self: "MazeGenerator", wall_name: str) -> str:
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
