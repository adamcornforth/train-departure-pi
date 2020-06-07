import time

from luma.core.image_composition import ImageComposition, ComposableImage

from boardrow import BoardRow


class Board:
    def __init__(self, device, interval=1.0):
        self.device = device
        self.composition = ImageComposition(self.device)

        self.rows = []

        self.interval = interval
        self.last_updated = 0.0

    def addRow(self, boardrow: BoardRow):
        """
        Add a row to paint on every Board tick
        """
        self.rows.append(boardrow)
        self.composition.add_image(boardrow.composableimage)

    def should_redraw(self):
        """
        Only requests a redraw after ``interval`` seconds have elapsed.
        """
        return time.monotonic() - self.last_updated > self.interval

    def tick(self):
        """
        Update and re-paint all the image compositions onto the board
        """
        for row in self.rows:
            row.tick()

        if not self.should_redraw():
            return

        for row in self.rows:
            if row.textimage.should_redraw():
                # Every time we redraw the content of the row, we have to re-add it to the composition
                row.textimage.update()
                self.rows.remove(row)
                self.composition.remove_image(row.composableimage)
                row.composableimage = ComposableImage(
                    row.textimage.image, row.position, row.offset
                )
                self.addRow(row)

        self.last_updated = time.monotonic()
