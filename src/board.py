import time

from TextImage import TextImage
from luma.core.image_composition import ImageComposition, ComposableImage


class Board():
    def __init__(self, device, interval=1.0):
        self.device = device
        self.composition = ImageComposition(self.device)

        self.compositions = []

        self.interval = interval
        self.last_updated = 0.0

    def addRow(self, textimage: TextImage, position: tuple = (0, 0), offset: tuple = (0, 0), scrolling=False):
        """
        Add a row to paint on every Board tick
        """
        composableimage = ComposableImage(textimage.image, position, offset)
        self.compositions.append({
            'composableimage': composableimage,
            'textimage': textimage,
            'scrolling': scrolling
        })

        self.composition.add_image(composableimage)

    def should_redraw(self):
        """
        Only requests a redraw after ``interval`` seconds have elapsed.
        """
        return time.monotonic() - self.last_updated > self.interval

    def tick(self):
        for composableimage in self.compositions:
            if composableimage['scrolling']:
                # Scrolling rows need their offsets incrementing every tick
                if composableimage['composableimage'].offset[0] > composableimage['composableimage'].width:
                    composableimage['composableimage'].offset = (0, 0)
                else:
                    composableimage['composableimage'].offset = (
                        composableimage['composableimage'].offset[0] + 1,
                        0
                    )

        """
        Update and re-paint all the image compositions onto the board
        """
        if not self.should_redraw():
            return

        for updatingimage in self.compositions:
            if updatingimage['textimage'].should_redraw():
                self.composition.remove_image(updatingimage['composableimage'])
                updatingimage['textimage'].update()
                self.compositions.remove(updatingimage)
                self.addRow(
                    updatingimage['textimage'],
                    updatingimage['composableimage'].position,
                    updatingimage['composableimage'].offset,
                    updatingimage['scrolling']
                )

        self.last_updated = time.monotonic()
