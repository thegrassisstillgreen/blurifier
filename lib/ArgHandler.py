import argparse
import os
import sys
from pathvalidate import is_valid_filename, sanitize_filename

## NEEDS TO CHECK IF IMAGES WITH GIVEN TYPE ARE IN THE DIRECTORY SPECIFIED
    ## ie. if given dir, and ext of jpg, check that dir if there are any jpg files before proceeding

class ArgHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        self.setupParser()
        self.args = self.parser.parse_args()
        self.argPackage = {
            'directory': None,
            'extension': None,
            'outfile': None,
            'enhancers': {
                'brightness': None,
                'contrast': None
            }
        }

    ## CONSIDER USING A DATA FILE FOR THIS FOR EASY ADDITION/REMOVAL OF ELEMENTS
    ## AND LESS LENGTHY METHOD -- COULD SIMPLY USE A FOR LOOP
    # Adds all required/optional arguments to the parser
    def setupParser(self):
        ## REQUIRED ARGUMENTS ##
        self.parser.add_argument(
            "image_directory", 
            help = "The directory with the images you would like to combine."
        )

        self.parser.add_argument(
            "image_extension", 
            help = "The file extension of the image files that should be used (only single file type allowed)"
        )
        
        ## OPTIONAL ARGUMENTS ##
        self.parser.add_argument(
            '-of',
            '--outfile',
            type=str,
            default="output",
            help="The desired name of the output file.\n(default: %(default)s.<input_img_ext>)"
        )

        self.parser.add_argument(
            "-br",
            "--brightness",
            type=float,
            default=1.0,
            help="The level of brightness to apply to input images to prior to combining.\n(default: %(default)s)"
        )
        self.parser.add_argument(
            "-ct", 
            "--contrast", 
            type=float,
            default=1.0,
            help="The level of contrast to apply to input images to prior to combining.\n(default: %(default)s)"
        )

    def checkValidDirectory(self):
        directory = self.args.image_directory

        if not os.path.isdir(directory):
            print("error: The directory provided is not valid or does not exist.", file=sys.stderr)
            print("Make sure that you provide the directory argument BEFORE the image extension argument.", file=sys.stderr)
            self.parser.print_usage(sys.stderr)
            sys.exit(1)

        print("Directory O.K.", file=sys.stderr)
        self.argPackage['directory'] = directory

    def checkValidExtension(self):
        extension = self.args.image_extension

        validImageExtensions = ["tif", "jpg", "jpeg", "gif", "png", "raw"]

        if extension not in validImageExtensions:
            print("error: The extension provided is not valid", file=sys.stderr)
            print("It must be one of the following types: {ext_list}".format(ext_list=", ".join(ext for ext in validImageExtensions)), file=sys.stderr)
            self.parser.print_usage(sys.stderr)
            sys.exit(1)
        
        print("Extension O.K.", file=sys.stderr)
        self.argPackage['extension'] = extension
    
    def checkFileWithExtensionInDir(self):
        directory = self.args.image_directory
        filepaths = ["{dir}\\{fn}".format(dir=directory, fn=filename) for filename in os.listdir(directory)]
        extension = self.args.image_extension

        for filepath in filepaths:
            if os.path.isfile(filepath) and filepath.endswith(extension):
                print("Files O.K.", file=sys.stderr)
                break
        else:
            print("error: No files with {ext} extension were found in {dir}".format(ext=extension, dir=directory), file=sys.stderr)
            sys.exit(1)

    def checkValidOutfile(self):
        filename = self.args.outfile

        if (not is_valid_filename(filename)):
            print("error: Some characters in your given output filename are invalid.")
            print("Suggested output filename: {suggested}".format(suggested=sanitize_filename(filename)))
            self.parser.print_usage(sys.stderr)
            sys.exit(1)
        
        if (len(filename) > 255):
            print("error: The length of your filename is too large.")
            self.parser.print_usage(sys.stderr)
            sys.exit(1)

        print("Output filename O.K.", file=sys.stderr)
        self.argPackage['outfile'] = filename

    def checkValidImageEffect(self):
        brightness = self.args.brightness
        contrast = self.args.contrast

        # .. some validation if any #

        print("Image effects O.K.", file=sys.stderr)
        self.argPackage['enhancers']['brightness'] = brightness
        self.argPackage['enhancers']['contrast'] = contrast
    
    def checkArgPackageNotEmpty(self):
        for argKey, argValue in self.argPackage.items():
            if type(argValue) is type(None):
                print("error: Did not receive a value for {arg}.".format(arg=argKey))
                self.parser.print_usage(sys.stderr)
                sys.exit(1)
        
        print("Arguments O.K.", file=sys.stderr)

    def checkArgsValid(self):
        self.checkValidDirectory()
        self.checkValidExtension()
        self.checkFileWithExtensionInDir()
        self.checkValidOutfile()
        self.checkValidImageEffect()
        self.checkArgPackageNotEmpty()
    
    def getArgPackage(self):
        return self.argPackage
def main():
    ah = ArgHandler()
    ah.checkArgsValid()
    argPackage = ah.getArgPackage()

if __name__ == '__main__':
    main()