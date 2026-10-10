from .parser import Configs, config_parser
from .curses_colors import init_colors
from .maze import MazeGenerator

__all__ = [
        'MazeGenerator',
        'Configs',
        'config_parser',
        'init_colors'
        ]

