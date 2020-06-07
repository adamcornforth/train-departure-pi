import time
from dataclasses import dataclass

from luma.core.image_composition import ComposableImage

from TextImage import TextImage


class BoardRow:
    def __init__(
        self,
        textimage: TextImage,
        position: tuple = (0, 0),
        offset: tuple = (0, 0),
        scrolling=False,
        direction="h",
        delay=0,
        initialdelay=None,
    ):
        self.initialdelay = initialdelay if initialdelay else delay
        self.delay = delay
        self.direction = direction
        self.scrolling = scrolling
        self.offset = offset
        self.position = position
        self.textimage = textimage

        self.last_delay_tick = 0.0
        self.composableimage = ComposableImage(textimage.image, position, offset)

    def should_tick_delay(self):
        return time.monotonic() - self.last_delay_tick > 1

    def tick(self):
        if self.should_tick_delay():
            if self.scrolling and self.delay:
                self.delay = self.delay - 1
            self.last_delay_tick = time.monotonic()

        if not self.delay:
            self.scroll()

    def scroll(self):
        if self.scrolling:
            if self.direction == "v":
                if self.composableimage.offset[1] > self.composableimage.height:
                    self.composableimage.offset = (0, 0)
                    self.delay = self.initialdelay
                else:
                    self.composableimage.offset = (
                        0,
                        self.composableimage.offset[1] + 1,
                    )
            else:
                if self.composableimage.offset[0] > self.composableimage.width:
                    self.composableimage.offset = (0, 0)
                    self.delay = self.initialdelay
                else:
                    self.composableimage.offset = (
                        self.composableimage.offset[0] + 1,
                        0,
                    )
