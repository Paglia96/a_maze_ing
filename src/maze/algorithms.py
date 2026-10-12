from .cell import Wall, Cell
from random import seed, choice
from time import sleep
from typing import cast, TYPE_CHECKING
import curses as c

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


def prim_algorithm(
    self: MazeGenerator,
    stdscr: c.window,
    palette: int,
    horizontal_offset: int,
    vertical_offset: int,
    seed_rand: int,
    seconds: float,
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
    cells: list[Cell] = [self._random_valid_starting_cell()]
    cells[0].is_visited = True
    while cells:
        current = choice(cells)
        try:
            wall = choice(self._valid_walls(current))
        except IndexError:  # choice riceve lista vuota
            cells.remove(current)
            continue
        x, y = current.adjacent_cell(cast(str, wall.name))
        adjacent = self[x][y]
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


def dfs(
    self: MazeGenerator,
    stdscr: c.window,
    palette: int,
    horizontal_offset: int,
    vertical_offset: int,
    seed_rand: int,
    seconds: float,
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
    stack: list[Cell] = [self._random_valid_starting_cell()]
    stack[0].is_visited = True
    while stack:
        current = stack.pop()
        CellWall = list[tuple[Cell, Wall]]
        closest: CellWall = self._valid_closest_cells(current)
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


def bfs(self: MazeGenerator, stdscr: c.window) -> str:
    """Find the shortest path using BFS.

    Args:
        stdscr: The curses window.

    Returns:
        The path directions, or an empty string if no path exists.
    """
    from collections import deque

    # resetta a ogni chiamata
    for row in self.maze:
        for cell in row:
            cell.explored = False
            cell.parent = None
            cell.is_path = False
            cell.entry = False
            cell.end = False

    palette = cast(int, self.conf["PALETTE"])
    horizontal_offset = cast(int, self.conf["HORIZONTAL_OFFSET"])
    vertical_offset = cast(int, self.conf["VERTICAL_OFFSET"])
    seconds = cast(float, self.conf["SECONDS"])

    entry_cell = self.coordinates_to_cell(self.entry, "Entry")
    exit_cell = self.coordinates_to_cell(self.exit, "Exit")
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
                if wall.name is None:
                    continue
                x, y = current.adjacent_cell(wall.name)
                adjacent = self[x][y]
                if not adjacent.explored:
                    adjacent.explored = True
                    adjacent.parent = current
                    adjacent.direction = self.give_direction(wall.name)
                    exploring.append(adjacent)

    if found_exit:
        curr: Cell | None = exit_cell
        path: list[str] = []
        self.path = ""
        while curr:
            curr.is_path = True
            if curr == entry_cell:
                break
            path.append(curr.direction)
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
            curr = curr.parent

    if not exploring and not found_exit:
        return ""
    path.reverse()
    self.path = "".join(path)
    return self.path
