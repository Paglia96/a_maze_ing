from .parser import config_parser
from time import sleep
from dataclasses import dataclass, field
from itertools import product, cycle
from typing import Callable
from .maze import *

from .curses_colors import init_colors
from typing import Generator
