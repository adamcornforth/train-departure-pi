import time

from TextImage import TextImage
from luma.core.image_composition import ImageComposition, ComposableImage


class Board():
    def __init__(self, device, interval=1.0):
        self.device = device
        self.composition = ImageComposition(self.device)

        self.compositions = []
        self.scrollingCompositions = []

        self.drawCompositions()
        self.interval = interval
        self.last_updated = 0.0

    def addRow(self, textimage: TextImage, position: tuple):
        """
        Add a row to paint on every Board tick
        """
        composableimage = ComposableImage(textimage.image, position)
        self.compositions.append({
            'composableimage': composableimage,
            'textimage': textimage
        })

    def addScrollingRow(self, textimage: TextImage, position: tuple):
        """
        Add a row to paint on every Board tick that also scrolls horizontally
        """
        self.addRow(textimage, position)
        self.scrollingCompositions.append(self.compositions.copy().pop()['composableimage'])

    def should_redraw(self):
        """
        Only requests a redraw after ``interval`` seconds have elapsed.
        """
        return time.monotonic() - self.last_updated > self.interval

    def tick(self):
        """
        Update and re-paint all the image compositions onto the board
        """
        if not self.should_redraw():
            return

        self.last_updated = time.monotonic()

        for composableimage in self.compositions:
            self.composition.remove_image(composableimage['composableimage'])

        for updatingimage in self.compositions:
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

        self.drawCompositions()
        self.composition.refresh()
        pass

    def drawCompositions(self):
        for composableimage in self.compositions:
            self.composition.add_image(composableimage['composableimage'])

