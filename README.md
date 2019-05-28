
# Blurifier

### Create interesting layered images (blurs) using this easy-to-use command-line program.

---

## What is a _**'blur'**_?

<img src="https://github.com/thegrassisstillgreen/blurifier/blob/master/example_blurs/example_blur_1.jpg" width=50% alt="Tim Hortons window-side blur" />

>The blur above was created using 50 photos, all taken from the window of a Tim Hortons in Toronto, Canada.

A **blur** is a collection of images that are then overlaid on top of another. Depending on the way it's used, the resulting image can be anything! It can end up interesting and abstract-looking, or it can look like trash. It's all about the source images that you decide to include!

---

## Getting started

Before using this program, make sure you have [Python 3]([https://www.python.org/downloads/](https://www.python.org/downloads/)) installed on your device.

Clone this repository to your device in the folder of your choice, navigate to the **Blurify** folder in the command line and run the following command:

`pip install -r requirements.txt`

This will ensure that you have all of the necessary libraries on your system to run the program.

Now that you have all of the requirements installed, while still inside the **Blurify** folder, run the following command:

`python example.py --help`

This will show you a usage message as well as both the required and optional arguments for this program. You **must** include the directory from which you would like it to retrieve the images as well as the type of images you would like to use.

For example, if I was to use the images included in this repository in the *imgs* folder, I would type the following command:

`python example.py path\to\imgs jpg `

*(where path\to\imgs is the path to the directory on your device)*

If all went well, there should be a new .jpg file in the *Blurify* folder called *output.jpg*. Go ahead and open it! It should look like this:

<img src="https://github.com/thegrassisstillgreen/blurifier/blob/master/example_blurs/result_1.jpg" width=25% alt="Example blur result" />

### Congratulations! You just created your first *blur*!

---

## Making your own

Making your own blurs should be pretty easy now. All you need to do is provide a directory and the extension of the images you would like to use! 

#### Things to consider:
1. **Image Dimensions**
	*	All input images must be the same size (both width and height) or you may experience some unexpected results.
2. **File Size**
	*	Be careful of the file size of the images you use. Before using several 4K images to try and create an ultra HD blur, I recommend testing the program on some moderately-sized images to test your computer's limits before going all-out!
3. **File Type**
	* There is no support for mixing up file types at the moment but will be covered in future updates!

*Note: If you check out the `example.py` file, you will see some comments explaining which method calls are required and which are optional. At this point in time, the only optional method is the `changeImageSize()` method which allows you to reduce the size of your input images for faster processing.*
