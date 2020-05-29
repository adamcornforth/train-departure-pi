import os
import sys
import time
import json

from luma_options import get_device
from luma.core.render import canvas
from PIL import ImageFont, Image
from luma.core.virtual import viewport, snapshot


def makeFont(name, size):
    font_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'fonts',
            name
        )
    )
    return ImageFont.truetype(font_path, size)


device = get_device()
font = makeFont("Dot Matrix Regular.ttf", 10)
fontBold = makeFont("Dot Matrix Bold.ttf", 10)
fontBoldTall = makeFont("Dot Matrix Bold Tall.ttf", 10)
fontBoldLarge = makeFont("Dot Matrix Bold.ttf", 40)

try:
    while True:
        # The luma.core.render.canvas class automatically creates an PIL.ImageDraw object of the correct dimensions
        # and bit depth suitable for the device, so you may then call the usual Pillow methods to draw onto the
        # canvas.
        #
        # As soon as the with scope is ended, the resultant image is automatically flushed to the device’s
        # display memory and the PIL.ImageDraw object is garbage collected.
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((3, 3), "Hello world", fill="yellow", font=font)

except KeyboardInterrupt:
    pass
except ValueError as err:
    print(f"Error: {err}")
except KeyError as err:
    print(f"Error: Please ensure the {err} environment variable is set")
