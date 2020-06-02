import os
import sys
import time

import json

from board import Board
from luma_options import get_device
from luma.core.render import canvas

try:
    device = get_device()
    # Time between redraws on the display
    interval = 0.02

    os.environ['TZ'] = 'Europe/London'
    time.tzset()

    board = Board(device, interval)

    while True:
        with canvas(device, background=board.composition()) as draw:
            board.tick()

except KeyboardInterrupt:
    pass
except ValueError as err:
    print(f"Error: {err}")
except KeyError as err:
    print(f"Error: Please ensure the {err} environment variable is set")
