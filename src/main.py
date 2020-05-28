import os
import sys
import time
import json

from luma_options import get_device
from luma.core.render import canvas
from luma.core.virtual import viewport, snapshot

device = get_device()

try:
    # Box and text rendered in portrait mode
    while True:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10, 40), "Hello World", fill="white")

except KeyboardInterrupt:
    pass
except ValueError as err:
    print(f"Error: {err}")
except KeyError as err:
    print(f"Error: Please ensure the {err} environment variable is set")