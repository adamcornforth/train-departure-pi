import time
import os

from TextImage import TextImage
from luma.core.image_composition import ImageComposition, ComposableImage
from PIL import ImageFont, ImageDraw


class Board():
    def __init__(self, device, interval=1.0):
        self.device = device
        self.composition = ImageComposition(self.device)

        self.compositions = []
        self.scrollingCompositions = []
        self.updatingCompositions = []

        self.drawComposition()
        self.interval = interval
        self.last_updated = 0.0

    def addRow(self, composableimage: ComposableImage):
        self.compositions.append(composableimage)

    def addUpdatingRow(self, composableimage: ComposableImage, textimage: TextImage):
        self.updatingCompositions.append({
            'composableimage': composableimage,
            'textimage': textimage
        })
        self.addRow(composableimage)

    def addScrollingRow(self, composableimage: ComposableImage):
        self.scrollingCompositions.append(composableimage)
        self.addRow(composableimage)

    def should_redraw(self):
        """
        Only requests a redraw after ``interval`` seconds have elapsed.
        """
        return time.monotonic() - self.last_updated > self.interval

    def tick(self):
        if not self.should_redraw():
            return

        self.last_updated = time.monotonic()

        for composableimage in self.compositions:
            self.composition.remove_image(composableimage)

        for k,updatingimage in enumerate(self.updatingCompositions):
            updatingimage['textimage'].update()
            updatingimage['composableimage'].image = ComposableImage(
                updatingimage['textimage'].image,
                updatingimage['composableimage'].position,
                updatingimage['composableimage'].offset
            ).image

        # Scrolling text
        for scrollingcomposition in self.scrollingCompositions:
            if scrollingcomposition.offset[0] > scrollingcomposition.width:
                scrollingcomposition.offset = (0, 0)
            else:
                scrollingcomposition.offset = (scrollingcomposition.offset[0] + 1, 0)

        self.drawComposition()
        self.composition.refresh()
        pass

    def drawComposition(self):
        for composableimage in self.compositions:
            self.composition.add_image(composableimage)

