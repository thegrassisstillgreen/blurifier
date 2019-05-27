from PIL import Image
import sys

class Img:
    def __init__(self, img):
        self.img = img
        self.pixels = None
        self.size = self.getSize()
        self.filepath = self.getFilePath()

    def setNewPixels(self, pixels):
        self.img.putdata(pixels)

        if pixels != self.getPixels():
            print("Pixel change unsuccessful...", file=sys.stderr)
            sys.exit(1)

        self.pixels = self.getPixels()

    def getPixels(self):
        return list(self.img.getdata())

    def getSize(self):
        return self.img.size
    
    def setSize(self, size):
        self.img.thumbnail(size, Image.ANTIALIAS)
        self.size = self.getSize()
        self.pixels = self.getPixels()

    def getFilePath(self):
        try:
            return self.img.filename
        except AttributeError:
            return None
