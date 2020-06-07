import os
import time
import json
import requests

from board import Board
from luma_options import get_device
from TextImage import TextImage
from PIL import ImageFont, ImageDraw
from luma.core.render import canvas


def renderDestinationRow(draw: ImageDraw, width, height):
    status = "On time"
    departureTime = data["departures"]["all"][0]["aimed_departure_time"]
    timeWidth, _ = draw.textsize(departureTime, font)
    statusWidth, _ = draw.textsize(status, font)

    draw.text((0, 0), departureTime, fill="yellow", font=font)
    destination = data["departures"]["all"][0]["destination_name"]
    draw.text((timeWidth + 5, 0), destination, fill="yellow", font=font)
    draw.text((width - statusWidth, 0), status, fill="yellow", font=font)


def renderCallingAt(draw: ImageDraw, width, height):
    callingAt = "Calling at:"

    draw.text((0, 0), callingAt, fill="yellow", font=font)


def renderCallingAtStations(draw: ImageDraw, width, height):
    draw.text((0, 0), timetable_stops, fill="yellow", font=font)


def renderAdditionalRow(draw: ImageDraw, width, height):
    nRow = "2nd:"
    draw.text((0, 0), nRow, fill="yellow", font=font)

    nTime = data["departures"]["all"][1]["aimed_departure_time"]
    nDestination = data["departures"]["all"][1]["destination_name"]
    nWidth, _ = draw.textsize(nRow, font)
    nTimeWidth, _ = draw.textsize(nTime, font)
    draw.text((nWidth + 5, 0), nTime, fill="yellow", font=font)
    draw.text((nWidth + nTimeWidth + 10, 0), nDestination, fill="yellow", font=font)

    status = "On time"
    statusWidth, _ = draw.textsize(status, font)
    draw.text((width - statusWidth, 0), status, fill="yellow", font=font)


def renderAdditionalRow3(draw: ImageDraw, width, height):
    nRow = "3rd:"
    draw.text((0, 0), nRow, fill="yellow", font=font)

    nTime = data["departures"]["all"][2]["aimed_departure_time"]
    nDestination = data["departures"]["all"][2]["destination_name"]
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
    draw.text(
        ((width / 2) - (textwidth / 2), 0),
        current_time,
        fill="yellow",
        font=fontBoldTall,
    )


def makeFont(name, size):
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "fonts", name))
    return ImageFont.truetype(font_path, size)


font = makeFont("Dot Matrix Regular.ttf", 10)
fontBold = makeFont("Dot Matrix Bold.ttf", 10)
fontBoldTall = makeFont("Dot Matrix Bold Tall.ttf", 10)
fontBoldLarge = makeFont("Dot Matrix Bold.ttf", 40)

try:
    device = get_device()
    # Time between redraws on the display
    interval = 0.025

    os.environ["TZ"] = "Europe/London"
    time.tzset()

    API_ID = os.environ.get("API_ID")
    API_KEY = os.environ.get("API_KEY")

    if not API_ID or not API_KEY:
        raise EnvironmentError("API_ID or API_KEY environment variables not set!")

    response = requests.get(
        "http://transportapi.com/v3/uk/train/station/EUS/live.json?app_id="
        + API_ID
        + "&app_key="
        + API_KEY
        + "&calling_at=MAN"
    )
    data = json.loads(response.text)
    # with open(os.path.dirname(os.path.realpath(__file__)) + '/departures.json') as json_file:
    #     data = json.load(json_file)

    response = requests.get(data["departures"]["all"][0]["service_timetable"]["id"])
    timetable = json.loads(response.text)
    # with open(os.path.dirname(os.path.realpath(__file__)) + '/timetable.json') as json_file:
    #     timetable = json.load(json_file)
    timetable_stops = ", ".join(
        [stop["station_name"] for stop in timetable["stops"][1:-1]]
    )

    board = Board(device, interval)

    board.addRow(TextImage(renderDestinationRow, device, device.width, 14, 10))
    if len(data["departures"]["all"]):
        with canvas(device) as draw:
            board.addRow(
                TextImage(
                    renderCallingAtStations,
                    device,
                    draw.textsize(timetable_stops, font)[0],
                    14,
                    10,
                ),
                (draw.textsize("Calling at:", font)[0], 14),
                scrolling=True,
                direction="h",
                delay=2,
            )
        board.addRow(TextImage(renderCallingAt, device, 40, 14, 10), (0, 14))
    if len(data["departures"]["all"]) > 2:
        board.addRow(
            TextImage(renderAdditionalRow3, device, device.width, 14, 4.5),
            (0, 28),
            scrolling=True,
            direction="v",
            delay=5,
        )
    if len(data["departures"]["all"]) > 1:
        board.addRow(
            TextImage(renderAdditionalRow, device, device.width, 14, 10),
            (0, 28),
            scrolling=(len(data["departures"]["all"]) > 2),
            direction="v",
            delay=5,
        )
    board.addRow(TextImage(renderClock, device, device.width, 14, 1), (0, 50))

    while True:
        with canvas(device, background=board.composition()) as draw:
            board.tick()
            time.sleep(0.025)
            board.composition.refresh()

except KeyboardInterrupt:
    pass
except ValueError as err:
    print(f"Error: {err}")
except KeyError as err:
    print(f"Error: Please ensure the {err} environment variable is set")
