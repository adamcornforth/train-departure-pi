import time
import os

from TextImage import TextImage
from luma.core.image_composition import ImageComposition, ComposableImage
from PIL import ImageFont, ImageDraw

class Board():
    def __init__(self, device, interval=1.0):
        self.device = device
        self.composition = ImageComposition(self.device)

        self.destinationRow = ComposableImage(
            TextImage(renderDestinationRow, self.device, self.device.width, 14).image,
            (0, 0)
        )
        self.callingAtStations = ComposableImage(
            TextImage(renderCallingAtStations, self.device, self.device.width * 2, 14).image,
            (0, 14)
        )
        self.callingAt = ComposableImage(
            TextImage(renderCallingAt, self.device, 40, 14).image,
            (0, 14)
        )
        self.additionalRow = ComposableImage(
            TextImage(renderAdditionalRow, self.device, self.device.width, 14).image,
            (0, 28)
        )
        self.clockImage = TextImage(renderClock, self.device, self.device.width, 14)
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
    draw.text((width - statusWidth, 0), status, fill="yellow", font=font)


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
    draw.text((width - statusWidth, 0), status, fill="yellow", font=font)

def makeFont(name, size):
    font_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'fonts',
            name
        )
    )
    return ImageFont.truetype(font_path, size)

font = makeFont("Dot Matrix Regular.ttf", 10)
fontBold = makeFont("Dot Matrix Bold.ttf", 10)
fontBoldTall = makeFont("Dot Matrix Bold Tall.ttf", 10)
fontBoldLarge = makeFont("Dot Matrix Bold.ttf", 40)