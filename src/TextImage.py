from PIL import Image, ImageDraw

# Inspired by: https://github.com/rm-hull/luma.examples/blob/master/examples/image_composition.py
class TextImage():
    def __init__(self, drawFunction, device, width, height):
        self.drawFunction = drawFunction
        self.width = width
        self.height = height
        self.deviceMode = device.mode

        self.image = Image.new(self.deviceMode, (self.width, self.height))
        self.update()

    def update(self):
        self.image = Image.new(self.deviceMode, (self.width, self.height))
        self.drawFunction(ImageDraw.Draw(self.image), self.width, self.height)
        pass