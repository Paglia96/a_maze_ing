from time import sleep
from enum import IntFlag
from dataclasses import dataclass, field
from itertools import product, cycle
from typing import Callable
from .parser import config_parser
from .maze import *

from .curses_colors import init_colors
from typing import Generator
