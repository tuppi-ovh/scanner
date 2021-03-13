"""
Document Scanner - Simplify the document scanning process.
Copyright (C) 2021 Vadim MUKHTAROV

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

For information on Document Scanner: tuppi.ovh@gmail.com
"""

import os
import inspect

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import Listbox
from PIL import ImageTk, Image, ImageEnhance

import config

CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

DEFAULT_INPUT_PATH = "/"
DEFAULT_INPUT_IMAGE_SIZE = 550
DEFAULT_OUTPUT_PATH = "/"

DEFAULT_PAD = 5
DEFAULT_CONTRAST = 200
DEFAULT_ROTATION = 0.0

# overwrite config
if config.DEFAULT_INPUT_PATH is not None:
    DEFAULT_INPUT_PATH = config.DEFAULT_INPUT_PATH
if config.DEFAULT_OUTPUT_PATH is not None:
    DEFAULT_OUTPUT_PATH = config.DEFAULT_OUTPUT_PATH


def reduceFilename(filename):
    length = len(filename)
    max_length = 40
    if length > max_length:
        filename = "..." + filename[(length - max_length):]
    return filename

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.outputImages = []
        self.logCounter = 0
        self.buildGui()

    def buildGuiCrop(self, frame, column_from, row, text, cmd):
        # crop label
        label = ttk.Label(frame, text = text)
        label.grid(column = column_from, row = row, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # crop spinbox
        value = StringVar()
        value.set(0)
        spinbox = Spinbox(
            frame,
            from_=0,
            to=100,
            increment=5,
            textvariable=value,
            width=6,
            command=cmd
            )
        spinbox.grid(column = column_from + 1, row = row, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # crop 2 spinbox
        value2 = StringVar()
        value2.set(100)
        spinbox2 = Spinbox(
            frame,
            from_=0,
            to=100,
            increment=5,
            textvariable=value2,
            width=6,
            command=cmd
            )
        spinbox2.grid(column = column_from + 2, row = row, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # return all
        return (value, value2)

    def buildGui(self):

        # Different inits
        self.title("Document Scanner")
        self.minsize(DEFAULT_INPUT_IMAGE_SIZE * 2, DEFAULT_INPUT_IMAGE_SIZE)

        # Frames
        self.controlFrame = ttk.Frame(self)
        self.controlFrame.grid(column = 0, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        self.buttonFrame = ttk.Frame(self.controlFrame)
        self.buttonFrame.grid(column = 0, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)        

        self.settingFrame = ttk.Frame(self.controlFrame)
        self.settingFrame.grid(column = 0, row = 1, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        self.inputImageFrame = ttk.LabelFrame(self, text = "Input Image")
        self.inputImageFrame.grid(column = 0, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
    
        self.outputImageFrame = ttk.LabelFrame(self, text = "Output Image")
        self.outputImageFrame.grid(column = 1, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD) 

        # Commands: button open image
        self.buttonInput = ttk.Button(self.buttonFrame, text = "Open Image", command = self.openFile)
        self.buttonInput.grid(column = 0, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: append
        self.buttonShow = ttk.Button(self.buttonFrame, text = "Append to PDF", command = self.appendImage)
        self.buttonShow.grid(column = 1, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: save
        self.buttonShow = ttk.Button(self.buttonFrame, text = "Save PDF", command = self.outputFile)
        self.buttonShow.grid(column = 2, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        # rotation label
        self.rotateLabel = ttk.Label(self.settingFrame, text = "Rotation:")
        self.rotateLabel.grid(column = 0, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # rotation spinbox
        self.rotateValue = StringVar()
        self.rotateValue.set(DEFAULT_ROTATION)
        self.rotateSpinBox = Spinbox(
            self.settingFrame,
            from_=-180,
            to=180,
            increment=0.2,
            textvariable=self.rotateValue,
            width=6,
            command=self.rotateImage
            )
        self.rotateSpinBox.grid(column = 1, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        # contrast label
        self.contrastLabel = ttk.Label(self.settingFrame, text = "Contrast:")
        self.contrastLabel.grid(column = 2, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # contrast spinbox
        self.contrastValue = StringVar()
        self.contrastValue.set(DEFAULT_CONTRAST)
        self.contrastSpinBox = Spinbox(
            self.settingFrame,
            from_=0,
            to=300,
            increment=10,
            textvariable=self.contrastValue,
            width=6,
            command=self.contrastImage
            )
        self.contrastSpinBox.grid(column = 3, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        # crop x
        self.cropLeftValue, self.cropRightValue = self.buildGuiCrop(
            frame = self.settingFrame,
            column_from = 0,
            row = 1,
            text = "Crop on X:",
            cmd = self.cropImage
        )
        # crop y
        self.cropTopValue, self.cropBottomValue = self.buildGuiCrop(
            frame = self.settingFrame,
            column_from = 3,
            row = 1,
            text = "Crop on Y:",
            cmd = self.cropImage
        )

        # log listbox
        self.logList = Listbox(self, height=6, width=70)
        self.logList.grid(column = 1, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        # empty images
        self.whiteColor = (255, 255, 255)
        emptyImg = Image.new("RGB", (DEFAULT_INPUT_IMAGE_SIZE, DEFAULT_INPUT_IMAGE_SIZE), self.whiteColor)
        emptyPhotoImg = ImageTk.PhotoImage(emptyImg)  
        # show input
        self.canvas = Canvas(self.inputImageFrame, width=DEFAULT_INPUT_IMAGE_SIZE, height=DEFAULT_INPUT_IMAGE_SIZE)  
        self.canvas.pack()
        self.canvasImage = self.canvas.create_image(DEFAULT_INPUT_IMAGE_SIZE/2, DEFAULT_INPUT_IMAGE_SIZE/2, anchor=CENTER, image=emptyPhotoImg) 
        self.canvas.image = emptyPhotoImg
        # show output
        self.outputCanvas = Canvas(self.outputImageFrame, width=DEFAULT_INPUT_IMAGE_SIZE, height=DEFAULT_INPUT_IMAGE_SIZE)  
        self.outputCanvas.pack()
        self.outputCanvasImage = self.outputCanvas.create_image(DEFAULT_INPUT_IMAGE_SIZE/2, DEFAULT_INPUT_IMAGE_SIZE/2, anchor=CENTER, image=emptyPhotoImg) 
        self.outputCanvas.image = emptyPhotoImg

    def log(self, message):
        self.logList.insert(0, " [{}] {}".format(self.logCounter, message))
        self.logCounter += 1

    def openFile(self):
        self.filename = filedialog.askopenfilename(
            initialdir=DEFAULT_INPUT_PATH, 
            title="Input File", 
            filetypes=(("image files","*.png"),("all files","*.*")) 
            )
        # scale 
        self.img = Image.open(self.filename)
        width, height = self.img.size
        ratio = min(DEFAULT_INPUT_IMAGE_SIZE / width, DEFAULT_INPUT_IMAGE_SIZE / height)
        self.reducedImg = self.img.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
        inputPhotoImg = ImageTk.PhotoImage(self.reducedImg)
        # default values
        self.rotateValue.set(DEFAULT_ROTATION)
        self.contrastValue.set(DEFAULT_CONTRAST)
        # show input
        self.canvas.itemconfig(self.canvasImage, image = inputPhotoImg)
        self.canvas.image = inputPhotoImg
        # process output
        self.processImage(image=self.reducedImg)
        # log
        self.log("Open file {}".format(reduceFilename(self.filename)))

    def rotateImage(self):
        self.processImage(image=self.reducedImg)

    def contrastImage(self):
        self.processImage(image=self.reducedImg)

    def cropImage(self):
        self.processImage(image=self.reducedImg)

    def appendImage(self):
        self.processImage(image=self.img, append=True)
        # log
        self.log("Append file {} to PDF ({})".format(reduceFilename(self.filename), len(self.outputImages)))

    def outputFile(self):
        self.processImage(image=self.img, save=True)
        # log
        self.log("Save PDF as {}".format(reduceFilename(self.filenamePdf)))
        self.log("------------------------------")

    def processImage(self, image=None, save=False, append=False):
        # rotate
        outputImg = image.rotate(float(self.rotateValue.get()), expand=0, fillcolor=self.whiteColor)
        # contrast
        enhancer = ImageEnhance.Contrast(outputImg)
        outputImg = enhancer.enhance(float(self.contrastValue.get()) * 0.01)
        # crop 
        width, height = outputImg.size
        left = width * float(self.cropLeftValue.get()) * 0.01
        top = height * float(self.cropTopValue.get()) * 0.01
        right = width * float(self.cropRightValue.get()) * 0.01
        bottom = height * float(self.cropBottomValue.get()) * 0.01
        outputImg = outputImg.crop((left, top, right, bottom)) 
        # scale
        width, height = outputImg.size
        ratio = min(DEFAULT_INPUT_IMAGE_SIZE / width, DEFAULT_INPUT_IMAGE_SIZE / height)
        outputPhotoImg = outputImg.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
        outputPhotoImg = ImageTk.PhotoImage(outputPhotoImg)
        # show output
        self.outputCanvas.itemconfig(self.outputCanvasImage, image = outputPhotoImg)
        self.outputCanvas.image = outputPhotoImg
        # append 
        if append:
            if outputImg.mode == 'RGBA':
                outputImg = outputImg.convert('RGB')
            self.outputImages.append(outputImg)
        # save
        if save:
            self.filenamePdf = filedialog.asksaveasfilename(
                initialdir = DEFAULT_OUTPUT_PATH, 
                title = "Output File", 
                defaultextension="*.*",
                filetypes = (("document files","*.pdf"),("all files","*.*")) )
            self.outputImages[0].save(self.filenamePdf, save_all=True, append_images=self.outputImages[1:])
            # clear output images 
            self.outputImages = []

root = Root()
root.mainloop()
