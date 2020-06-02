import os
import sys
import time

import json

from luma_options import get_device
from luma.core.render import canvas
from PIL import ImageFont, ImageDraw, Image
from luma.core.image_composition import ImageComposition, ComposableImage
from luma.core.virtual import viewport, snapshot


# From: https://github.com/rm-hull/luma.examples/blob/master/examples/image_composition.py
class TextImage():
    def __init__(self, drawFunction, device, width, height):
        self.drawFunction = drawFunction
        self.width = width
        self.height = height
        self.deviceMode = device.mode

        self.image = Image.new(self.deviceMode, (self.width, self.height))
        self.update()

    def update(self):
        self.image = Image.new(self.deviceMode, (self.width, self.height))
        self.drawFunction(ImageDraw.Draw(self.image), self.width, self.height)
        pass


class Board():
    def __init__(self, device, interval=1.0):
        self.composition = ImageComposition(device)

        self.destinationRow = ComposableImage(
            TextImage(renderDestinationRow, device, device.width, 14).image,
            (0, 0)
        )
        self.callingAtStations = ComposableImage(
            TextImage(renderCallingAtStations, device, device.width * 2, 14).image,
            (0, 14)
        )
        self.callingAt = ComposableImage(
            TextImage(renderCallingAt, device, 40, 14).image,
            (0, 14)
        )
        self.additionalRow = ComposableImage(
            TextImage(renderAdditionalRow, device, device.width, 14).image,
            (0, 28)
        )
        self.clockImage = TextImage(renderClock, device, device.width, 14)
        self.clock = ComposableImage(
            self.clockImage.image,
            (0, 50)
        )

        self.drawComposition()
        self.interval = interval
        self.last_updated = 0.0

    def should_redraw(self):
        """
        Only requests a redraw after ``interval`` seconds have elapsed.
        """
        return time.monotonic() - self.last_updated > self.interval

    def tick(self):
        if self.should_redraw() == False:
            return

        self.last_updated = time.monotonic()

        self.composition.remove_image(self.destinationRow)
        self.composition.remove_image(self.callingAtStations)
        self.composition.remove_image(self.callingAt)
        self.composition.remove_image(self.additionalRow)
        self.composition.remove_image(self.clock)

        self.clockImage.update()
        self.clock = ComposableImage(
            self.clockImage.image,
            (0, 50)
        )

        if self.callingAtStations.offset[0] > self.callingAtStations.width:
            self.callingAtStations.offset = (0, 0)
        else:
            self.callingAtStations.offset = (self.callingAtStations.offset[0] + 1, 0)

        self.drawComposition()
        self.composition.refresh()
        pass

    def drawComposition(self):
        self.composition.add_image(self.destinationRow)
        self.composition.add_image(self.callingAtStations)
        self.composition.add_image(self.callingAt)
        self.composition.add_image(self.additionalRow)
        self.composition.add_image(self.clock)


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


def renderCallingAt(draw: ImageDraw, width, height):
    callingAt = "Calling at:"

    draw.text((0, 0), callingAt, fill="yellow", font=font)


def renderCallingAtStations(draw: ImageDraw, width, height):
    callingAt = "Calling at:"
    callingAtWidth = draw.textsize(callingAt, font)[0]
    callingAtStations = "Clapham Junction, East Croydon, Blackfriars, London, London St Pancras"

    draw.text((callingAtWidth, 0), callingAtStations, fill="yellow", font=font)


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


try:
    device = get_device()
    # Time between redraws on the display
    interval = 0.02

    font = makeFont("Dot Matrix Regular.ttf", 10)
    fontBold = makeFont("Dot Matrix Bold.ttf", 10)
    fontBoldTall = makeFont("Dot Matrix Bold Tall.ttf", 10)
    fontBoldLarge = makeFont("Dot Matrix Bold.ttf", 40)

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
