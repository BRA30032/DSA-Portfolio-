# __init__.py
# Makes the data folder a Python package so imports work cleanly.

from .airports   import AIRPORTS
from .city_map   import CITY_MAP
from .flight_data import AIRCRAFTS, GATES, STATUS_POOL
from .colors     import GREEN, RED, YELLOW, BLUE, CYAN, GREY, BOLD, RESET, STATUS_COLORS
