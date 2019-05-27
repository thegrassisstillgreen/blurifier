from glob import glob
from PIL import Image, ImageEnhance
from tqdm import tqdm
import os
import sys
from lib.Imager import Img

## TODO:
##  - NEED FASTER ALGO FOR AVERAGING PIXELS (CURRENT IS FINE FOR SHRUNKEN IMAGES, BUT NOT ACTUAL SIZE)
##  - DEAL WITH IMAGES OF DIFFERENT SIZES? MAKE ALL IMAGES SAME SIZE: GIVEN SIZE? IDK
##  - SEPARATE INTO MULTIPLE CLASSES:
##      - IMAGER IS A BASIC CLASS THAT HAS THE IMAGES SIZE INFO, PIXEL INFO, ETC. -- NO METHODS, JUST ATTRS
##      - PHOTOREADER GETS THE PHOTOS, ENHANCES THEM, GETS THE PIXEL INFO
##      - IMAGECOMBINER GETS THE PIXEL INFO FROM PHOTO READER AND ADDS/AVERAGES THE INFO


##  - ADDED NEW IMG CLASS THAT HOLDS ALL IMAGE ATTRS
##      - CHANGE METHODS TO WORK WITH PIXEL DATA INSTEAD OF THE ACTUAL IMAGE -- PERHAPS SPEED THINGS UP
class PhotoReader:
    def __init__(self, args):
        self.imgDir = args['directory']
        self.imgExt = args['extension'] # the extension of images to gather
        self.imgOut = args['outfile']
        self.imgs = None # all of the images
        self.imgRef = None
        self.pixelSum = None
        self.pixelAvg = None
        self.imgEnhancers = args['enhancers']

    ## Changed
    def getImages(self):
        self.imgs = []
        imgFiles = [imgFile for imgFile in glob('{dir}\*.{ext}'.format(dir=self.imgDir, ext=self.imgExt))]
        for imgFile in imgFiles:
            img = Image.open(imgFile)
            imgAttrs = packImageAttributes(imgFile, img)
            newImg = Img(img, imgAttrs)
            self.imgs.append(newImg)

    ## Changed
    def packImageAttributes(self, imgFile, img):
        path = imgFile
        filename = os.path.basename(imgFile)
        extension = filename.split(".")[-1]
        pixels = list(img.getdata())
        size = img.size

        imageAttrs = {
            'path': path,
            'filename': filename,
            'extension': extension,
            'pixels': pixels,
            'size': size
        }

        return imageAttrs

    '''
    def enhanceImages(self):
        baseValue = 1.0
        eDispatcher = {
            'brightness': ImageEnhance.Brightness,
            'contrast': ImageEnhance.Contrast
        }

        for enhancer, evalue in self.imgEnhancers.items():
            if evalue == baseValue:
                continue

            print("Enhancing image {enhancer}...".format(enhancer=enhancer))
            self.imgs = [eDispatcher[enhancer](img).enhance(evalue) for img in tqdm(self.imgs)]
    '''
    '''
    def shrinkImages(self, maxSize):
        for img in self.imgs:
            img = img.thumbnail(maxSize, Image.ANTIALIAS)
    '''
    def createEmptyPixelSlots(self):
        self.imgRef = self.imgs[0]
        pixelInfo = list(self.imgRef.getdata())
        emptyPixels = [[0, 0, 0] for pixelTuple in pixelInfo]

        return emptyPixels

    def getQuickAvg(self):
        pixelSum = self.createEmptyPixelSlots()
        imgs = self.imgs

        print("Adding up all pixel values...", file=sys.stderr)
        for img in tqdm(imgs):
            pixels = list(img.getdata())
            for pixelIndex, pixelGroup in enumerate(pixels):
                pixelSum[pixelIndex] = [sum(RGB) for RGB in zip(pixelSum[pixelIndex], pixelGroup)]
                '''
                for RGB in range(3):
                    pixelSum[pixelIndex][RGB] += pixelGroup[RGB]
                '''
        print("Averaging each pixel...", file=sys.stderr)
        pixelAvg = [[RGB // len(imgs) for RGB in pixel] for pixel in tqdm(pixelSum)]

        self.pixelAvg = pixelAvg

    def getPixelAvg(self):
        numElems = 0
        pixelAvg = self.createEmptyPixelSlots()
        imgs = self.imgs

        for num, img in enumerate(imgs):
            print("Processing image {num}".format(num=num+1))
            pixels = list(img.getdata())
            numElems += 1
            for pixelId, pixel in enumerate(tqdm(pixels)):
                for RGB in range(3):
                    pixelAvg[pixelId][RGB] = (numElems * pixelAvg[pixelId][RGB] + pixel[RGB]) / (numElems + 1)
        
        self.pixelAvg = pixelAvg

    def formatPixelData(self):
        for pixelId, pixel in enumerate(self.pixelAvg):
            self.pixelAvg[pixelId] = tuple([int(RGB) for RGB in pixel])

    def Results(self):
        newImg = Image.new(self.imgRef.mode, self.imgRef.size)
        self.formatPixelData()
        newImg.putdata(self.pixelAvg)
        newImg.show()
        newImg.save(self.imgOut + "." + self.imgExt)