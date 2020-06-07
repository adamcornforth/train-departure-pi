import copy
import time

from TextImage import TextImage
from luma.core.image_composition import ImageComposition, ComposableImage


class Board:
    def __init__(self, device, interval=1.0):
        self.device = device
        self.composition = ImageComposition(self.device)

        self.compositions = []

        self.interval = interval
        self.last_updated = 0.0
        self.last_delay_tick = 0.0

    def addRow(
        self,
        textimage: TextImage,
        position: tuple = (0, 0),
        offset: tuple = (0, 0),
        scrolling=False,
        direction="h",
        delay=0,
        initialdelay=None,
    ):
        """
        Add a row to paint on every Board tick
        """
        composableimage = ComposableImage(textimage.image, position, offset)

        if not initialdelay:
            initialdelay = delay

        self.compositions.append(
            {
                "composableimage": composableimage,
                "textimage": textimage,
                "scrolling": scrolling,
                "direction": direction,
                "delay": delay,
                "initialdelay": initialdelay,
            }
        )

        self.composition.add_image(composableimage)

    def should_redraw(self):
        """
        Only requests a redraw after ``interval`` seconds have elapsed.
        """
        return time.monotonic() - self.last_updated > self.interval

    def should_tick_delay(self):
        return time.monotonic() - self.last_delay_tick > 1

    def tick(self):
        if self.should_tick_delay():
            for composableimage in self.compositions:
                if composableimage["scrolling"] and composableimage["delay"]:
                    composableimage["delay"] = composableimage["delay"] - 1
            self.last_delay_tick = time.monotonic()

        for composableimage in self.compositions:
            if composableimage["scrolling"] and not composableimage["delay"]:
                if composableimage["direction"] == "v":
                    # Scrolling rows need their offsets incrementing every tick
                    if (
                        composableimage["composableimage"].offset[1]
                        > composableimage["composableimage"].height
                    ):
                        composableimage["composableimage"].offset = (0, 0)
                        composableimage["delay"] = composableimage.get("initialdelay")
                    else:
                        composableimage["composableimage"].offset = (
                            0,
                            composableimage["composableimage"].offset[1] + 1,
                        )
                else:
                    # Scrolling rows need their offsets incrementing every tick
                    if (
                        composableimage["composableimage"].offset[0]
                        > composableimage["composableimage"].width
                    ):
                        composableimage["composableimage"].offset = (0, 0)
                        composableimage["delay"] = composableimage.get("initialdelay")
                    else:
                        composableimage["composableimage"].offset = (
                            composableimage["composableimage"].offset[0] + 1,
                            0,
                        )

        """
        Update and re-paint all the image compositions onto the board
        """
        if not self.should_redraw():
            return

        for updatingimage in self.compositions:
            if updatingimage["textimage"].should_redraw():
                updatingimage["textimage"].update()
                self.compositions.remove(updatingimage)
                self.composition.remove_image(updatingimage["composableimage"])
                self.addRow(
                    updatingimage["textimage"],
                    updatingimage["composableimage"].position,
                    updatingimage["composableimage"].offset,
                    updatingimage["scrolling"],
                    updatingimage["direction"],
                    updatingimage["delay"],
                    updatingimage["initialdelay"],
                )

        self.last_updated = time.monotonic()
