import os
import time

from board import Board
from luma_options import get_device
from TextImage import TextImage
from PIL import ImageFont, ImageDraw
from luma.core.render import canvas


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
    callingAtStations = "Clapham Junction, East Croydon, Blackfriars, London St Pancras"

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


def renderClock(draw: ImageDraw, width, height):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    textwidth, _ = draw.textsize(current_time, fontBoldTall)
    draw.text(((width / 2) - (textwidth / 2), 0), current_time, fill="yellow", font=fontBoldTall)


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

try:
    device = get_device()
    # Time between redraws on the display
    interval = 0.02

    os.environ['TZ'] = 'Europe/London'
    time.tzset()

    board = Board(device, interval)

    board.addRow(
        TextImage(renderDestinationRow, device, device.width, 14, 5),
        (0, 0)
    )
    board.addRow(
        TextImage(renderCallingAtStations, device, device.width * 2, 14, 0.025),
        (0, 14),
        scrolling=True
    )
    board.addRow(
        TextImage(renderCallingAt, device, 40, 14, 5),
        (0, 14)
    )
    board.addRow(
        TextImage(renderAdditionalRow, device, device.width, 14, 5),
        (0, 28)
    )
    board.addRow(
        TextImage(renderClock, device, device.width, 14, 1),
        (0, 50)
    )

    board.drawCompositions()

    while True:
        with canvas(device, background=board.composition()) as draw:
            time.sleep(0.025)
            board.tick()

except KeyboardInterrupt:
    pass
except ValueError as err:
    print(f"Error: {err}")
except KeyError as err:
    print(f"Error: Please ensure the {err} environment variable is set")