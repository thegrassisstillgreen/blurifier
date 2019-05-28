from glob import glob
from PIL import Image
from lib.Imager import Img
from tqdm import tqdm
import sys

class ImgCombiner:
    def __init__(self, args):
        self.imgDir = args['directory']
        self.imgExt = args['extension']
        self.outFilename = args['outfile']
        
        self.imgs = []
        self.imgRef = None
        self.imgOut = None

    # Collects all of the file paths from this object's directory, then creates a custom image object for each one.
    # Also creates an image reference that will later be used to create the output image.
    def getImages(self):
        # Collect all the paths for the images in the given directory with the given extension
        imgFiles = [imgFile for imgFile in glob('{dir}\*.{ext}'.format(dir=self.imgDir, ext=self.imgExt))]
        
        print("Getting images...", file=sys.stderr)
        for imgFile in tqdm(imgFiles):
            img = Image.open(imgFile)
            self.imgs.append(Img(img))
        
        self.imgRef = self.imgs[0]

    # Changes the size of all images to fit within the given width and height. If the provided dimensions
    # are larger than those of the images there will be no change (consider renaming this method to reflect that...).
    def changeImageSize(self, imgWidth, imgHeight):
        newSize = (imgWidth, imgHeight)

        print("Resizing images...", file=sys.stderr)
        for img in tqdm(self.imgs):
            img.setSize(newSize)

    # This creates an 'empty' (zero-filled) 2D list of integers to hold the sum/avg pixels (depending on which method will use)
    # which will eventually be used to form the output image.
    def createEmptyPixels(self):
        pixelInfo = list(self.imgRef.getPixels())
        emptyPixels = [[0, 0, 0] for RGB in pixelInfo]

        return emptyPixels

    ## NOTE: The following two methods provide the same results, only they are different algorithms. Still testing
    ## the better algorithm...

    # This takes the average of all pixels by first collecting the sum of every pixel in every image across all images.
    # It then goes through this list and calculates the average by dividing each value by the number of elements.
    ## NOTE: Seems to be the faster method to average pixels, yet more for loops... investigate why!
    def getAveragePixels(self):
        pixelSum = self.createEmptyPixels()
        imgs = self.imgs
        numElems = len(imgs)

        print("Averaging pixels...", file=sys.stderr)
        for img in tqdm(imgs):
            pixels = img.getPixels()

            # In each pixel tuple, get the sums of the corresponding pixel tuples (aka. pixel info at x=1, y=1 in source 
            # image added to x=1, y=1 in the sum list)
            for pixelIndex, pixelGroup in enumerate(pixels):
                pixelSum[pixelIndex] = [sum(RGB) for RGB in zip(pixelSum[pixelIndex], pixelGroup)]

        pixelAvg = [[RGBValue // numElems for RGBValue in pixel] for pixel in tqdm(pixelSum)]

        return pixelAvg

    # Takes the gradual average for each pixel in all images using the following equation:
    # (n * a + s) / (n + 1), where:
    # n --> number of pixels currently averaged
    # a --> current average of the pixels
    # s --> new value to add to the pixel average
    def getQuickAverage(self):
        numElems = 0
        pixelAvg = self.createEmptyPixels()
        imgs = self.imgs

        print("Averaging pixels...", file=sys.stderr)
        for num, img in enumerate(tqdm(imgs)):
            pixels = img.getPixels() # This method takes a long time (depending on image size) -- try to find asynchronus solution?
            numElems += 1
            for pixelId, pixel in enumerate(pixels):
                for RGB in range(3):
                    pixelAvg[pixelId][RGB] = (numElems * pixelAvg[pixelId][RGB] + pixel[RGB]) / (numElems + 1)

        return pixelAvg

    # Goes through the list of pixels and formats it for the output image by converting every pixel RGB group
    # into a tuple.
    def formatPixelData(self, pixelData):
        for pixelId, pixel in enumerate(tqdm(pixelData)):
            pixelData[pixelId] = tuple([int(RGBValue) for RGBValue in pixel])
        
        return pixelData

    # Creates an empty Img object for the output image using the object's imgRef attribute for its size data.
    def createOutputImage(self):
        return Img(Image.new("RGB", self.imgRef.getSize()))

    # This is a small wrapper function that gets the average pixels from the images, formats them, creates the output image,
    # adds its data, shows it, and saves it.
    ## NOTE: This method may do too many different things... consider separating it up later between different methods.
    def combineImages(self):
        avgPixels = self.getQuickAverage()
        #avgPixels = self.getAveragePixels()
        print("Formatting pixel data...", file=sys.stderr)
        formattedPixels = self.formatPixelData(avgPixels)

        self.imgOut = self.createOutputImage()
        self.imgOut.setNewPixels(formattedPixels)

        print("Showing new image...", file=sys.stderr)
        self.imgOut.img.show()
        self.imgOut.img.save(self.outFilename + "." + self.imgExt)


