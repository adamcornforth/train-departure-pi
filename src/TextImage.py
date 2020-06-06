import time
from PIL import Image, ImageDraw


# Inspired by: https://github.com/rm-hull/luma.examples/blob/master/examples/image_composition.py
class TextImage():
    def __init__(self, drawFunction, device, width, height, interval=1.0):
        self.drawFunction = drawFunction
        self.width = width
        self.height = height
        self.deviceMode = device.mode
        self.interval = interval
        # Trigger first update immediately
        self.last_updated = time.monotonic() - self.interval

        self.image = Image.new(self.deviceMode, (self.width, self.height))
        self.update()

    def should_redraw(self):
        """
        Only requests a redraw after ``interval`` seconds have elapsed.
        """
        return time.monotonic() - self.last_updated > self.interval

    def update(self):
        self.last_updated = time.monotonic()

        self.image = Image.new(self.deviceMode, (self.width, self.height))
        self.drawFunction(ImageDraw.Draw(self.image), self.width, self.height)
