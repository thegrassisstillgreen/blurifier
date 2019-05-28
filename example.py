from lib.PhotoReader import PhotoReader
from lib.ArgHandler import ArgHandler
from lib.ImgCombiner import ImgCombiner

def main():
    # !REQUIRED!
    # Check that the arguments provided are valid and then get the packaged arguments.
    ah = ArgHandler()
    ah.checkArgsValid()
    argPackage = ah.getArgPackage()

    # !REQUIRED!
    # Create a new combiner object using the argument package from above and get the images from directory.
    ic = ImgCombiner(argPackage)
    ic.getImages()

    # !OPTIONAL!
    # Change the size of the images to be within certain dimensions to speed up the process
    ## NOTE: I have had troubles with collections of large images (4k resolution) freezing up my computer.
    ##       Unsure whether limitation of my hardware but reducing the size of the images helps to avoid this.
    ic.changeImageSize(250, 250)

    # !REQUIRED!
    # Process all photo info and then creates, shows, and saves the new image.
    ic.combineImages()
    
if __name__ == '__main__':
    main()
