import os
import sys
import time

import json

from luma_options import get_device
from luma.core.render import canvas
from PIL import ImageFont, ImageDraw, Image
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


def renderClock(draw: ImageDraw, width, height):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    textwidth, _ = draw.textsize(current_time, fontBoldTall)
    draw.text(((width / 2) - (textwidth / 2), 0), current_time, fill="yellow", font=fontBoldTall)


def renderDestinationRow(draw: ImageDraw, width, height):
    status = "Exp 14:44"
    departureTime = "14:29"
    timeWidth, _ = draw.textsize(departureTime, font)
    statusWidth, _ = draw.textsize(status, font)

    draw.text((0, 0), departureTime, fill="yellow", font=font)
    draw.text((timeWidth + 5, 0), "London St Pancras", fill="yellow", font=font)
    draw.text((device.width - statusWidth, 0), status, fill="yellow", font=font)


def renderCallingAtRow(draw: ImageDraw, width, height):
    callingAt = "Calling at:"
    callingAtWidth, _ = draw.textsize(callingAt, font)

    draw.text((0, 0), callingAt, fill="yellow", font=font)
    draw.text((callingAtWidth + 5, 0), "Clapham Junction, East Croydon", fill="yellow", font=font)

def renderAdditionalRow(draw: ImageDraw, width, height):
    nRow = "3rd:"
    draw.text((0, 0), nRow, fill="yellow", font=font)

    nTime = "14:51"
    nDestination = "Moorgate"
    nWidth, _ = draw.textsize(nRow, font)
    nTimeWidth, _ = draw.textsize(nTime, font)
    draw.text((nWidth + 5, 0), nTime, fill="yellow", font=font)
    draw.text((nWidth + nTimeWidth + 10, 0), nDestination, fill="yellow", font=font)

    status = "On time"
    statusWidth, _ = draw.textsize(status, font)
    draw.text((device.width - statusWidth, 0), status, fill="yellow", font=font)


def drawAll(display):
    destinationRow = snapshot(device.width, 14, renderDestinationRow, interval=1)
    callingAtRow = snapshot(device.width, 14, renderCallingAtRow, interval=1)
    additionalRow = snapshot(device.width, 14, renderAdditionalRow, interval=1)
    clock = snapshot(device.width, 14, renderClock, interval=1)

    display.add_hotspot(destinationRow, (0, 0))
    display.add_hotspot(callingAtRow, (0, 14))
    display.add_hotspot(additionalRow, (0, 28))
    display.add_hotspot(clock, (0, 50))

    return display


try:
    device = get_device()
    font = makeFont("Dot Matrix Regular.ttf", 10)
    fontBold = makeFont("Dot Matrix Bold.ttf", 10)
    fontBoldTall = makeFont("Dot Matrix Bold Tall.ttf", 10)
    fontBoldLarge = makeFont("Dot Matrix Bold.ttf", 40)

    os.environ['TZ'] = 'Europe/London'
    time.tzset()
    display = viewport(device, device.width, device.height)
    display = drawAll(display)

    while True:
        display.refresh()

except KeyboardInterrupt:
    pass
except ValueError as err:
    print(f"Error: {err}")
except KeyError as err:
    print(f"Error: Please ensure the {err} environment variable is set")
