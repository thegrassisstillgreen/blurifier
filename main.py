import sys
import os
import time
from lib.PhotoReader import PhotoReader
from lib.ArgHandler import ArgHandler
from lib.ImgCombiner import ImgCombiner

def main():
    ## Make sure that the given arguments are valid and then package them up to be used
    ah = ArgHandler()
    ah.checkArgsValid()
    argPackage = ah.getArgPackage()

    ic = ImgCombiner(argPackage)
    ic.getImages()
    #ic.changeImageSize(2000, 2000)
    #ic.extractPixelInfo()
    print("Starting...")
    start = time.time()
    ic.combineImages()
    end = time.time()

    print("results: {m1time}".format(m1time=(end - start)))

    '''
    pr = PhotoReader(argPackage)
    
    print("Getting images...")
    pr.getImages()
    #print("Shrinking images...")
    #pr.shrinkImages((1000,1000))
    print("Applying image effects...")
    pr.enhanceImages()

    pr1 = pr
    pr2 = pr
    
    print("Starting method 1...")
    startMethod1 = time.time()
    pr1.getQuickAvg()
    endMethod1 = time.time()
    
    print("Starting method 2")
    startMethod2 = time.time()
    pr2.getPixelAvg()
    endMethod2 = time.time()
    '''
    '''
    print("Showing results...")
    pr1.Results()
    pr2.Results()
    '''
    '''
    print("Method 1: {m1time}".format(m1time=(endMethod1 - startMethod1)))
    print("Method 2: {m2time}".format(m2time=(endMethod2 - startMethod2)))
    '''
if __name__ == '__main__':
    main()
