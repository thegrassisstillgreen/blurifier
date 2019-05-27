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
    
    def createEmptyImage(self):
        return Img(Image.new("RGB", self.imgRef.getSize()))

    def getImages(self):
        # Collect all the paths for the images in the given directory with the given extension
        imgFiles = [imgFile for imgFile in glob('{dir}\*.{ext}'.format(dir=self.imgDir, ext=self.imgExt))]
        
        print("Getting images...", file=sys.stderr)
        for imgFile in tqdm(imgFiles):
            img = Image.open(imgFile) # Create a PIL image object
            self.imgs.append(Img(img)) # Create custom image object from PIL image
        
        self.setImageRef()
    
    def setImageRef(self):
        self.imgRef = self.imgs[0]

    # Check to see what this does when provide larger than existing image size
    def changeImageSize(self, imgWidth, imgHeight):
        newSize = (imgWidth, imgHeight)
        
        print("Resizing images...", file=sys.stderr)
        for img in tqdm(self.imgs):
            img.setSize(newSize)
    '''
    def extractPixelInfo(self):
        print("Extracting pixel info...", file=sys.stderr)
        for img in tqdm(self.imgs):
            img.setPixels()
    '''
    def createEmptyPixels(self):
        pixelInfo = list(self.imgRef.getPixels())
        emptyPixels = [[0, 0, 0] for RGB in pixelInfo]

        return emptyPixels

    def getAveragePixels(self):
        pixelSum = self.createEmptyPixels()
        imgs = self.imgs
        numElems = len(imgs)

        print("Averaging pixels...", file=sys.stderr)
        for img in tqdm(imgs):
            pixels = img.getPixels()

            for pixelIndex, pixelGroup in enumerate(pixels):
                pixelSum[pixelIndex] = [sum(RGB) for RGB in zip(pixelSum[pixelIndex], pixelGroup)]

        pixelAvg = [[RGBValue // numElems for RGBValue in pixel] for pixel in tqdm(pixelSum)]

        return pixelAvg

    def getQuickAverage(self):
        numElems = 0
        pixelAvg = self.createEmptyPixels()
        imgs = self.imgs

        print("Averaging pixels...", file=sys.stderr)
        for num, img in enumerate(tqdm(imgs)):
            pixels = img.getPixels()
            numElems += 1
            for pixelId, pixel in enumerate(pixels):
                for RGB in range(3):
                    pixelAvg[pixelId][RGB] = (numElems * pixelAvg[pixelId][RGB] + pixel[RGB]) / (numElems + 1)

        return pixelAvg

    def combineImages(self):
        avgPixels = self.getQuickAverage()
        #avgPixels = self.getAveragePixels()
        # Format pixel data
        print("Formatting pixel data...", file=sys.stderr)
        for pixelId, pixel in enumerate(tqdm(avgPixels)):
            avgPixels[pixelId] = tuple([int(RGBValue) for RGBValue in pixel])

        self.imgOut = self.createEmptyImage()
        self.imgOut.setNewPixels(avgPixels)

        print("Showing new image...", file=sys.stderr)
        self.imgOut.img.show()
        self.imgOut.img.save(self.outFilename + "." + self.imgExt)


