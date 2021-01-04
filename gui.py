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
from PIL import ImageTk, Image, ImageEnhance

import config

CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

DEFAULT_INPUT_PATH = "/"
DEFAULT_INPUT_IMAGE_SIZE = 550
DEFAULT_OUTPUT_PATH = "/"

DEFAULT_PAD = 10
DEFAULT_CONTRAST = 2.0
DEFAULT_ROTATION = 0.0

# overwrite config
if config.DEFAULT_INPUT_PATH is not None:
    DEFAULT_INPUT_PATH = config.DEFAULT_INPUT_PATH
if config.DEFAULT_OUTPUT_PATH is not None:
    DEFAULT_OUTPUT_PATH = config.DEFAULT_OUTPUT_PATH

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Document Scanner")
        # width & height
        self.minsize(DEFAULT_INPUT_IMAGE_SIZE * 2, DEFAULT_INPUT_IMAGE_SIZE)
 
        self.labelFrame = ttk.LabelFrame(self, text = "Commands")
        self.labelFrame.grid(column = 0, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        self.inputImageFrame = ttk.LabelFrame(self, text = "Input Image")
        self.inputImageFrame.grid(column = 0, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
    
        self.outputImageFrame = ttk.LabelFrame(self, text = "Output Image")
        self.outputImageFrame.grid(column = 1, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD) 

        # Commands: button input file
        self.buttonInput = ttk.Button(self.labelFrame, text = "Open Image", command = self.openFile)
        self.buttonInput.grid(column = 0, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: rotate
        self.rotateFrame = ttk.LabelFrame(self.labelFrame, text = "Rotate")
        self.rotateFrame.grid(column = 1, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: contrast
        self.contrastFrame = ttk.LabelFrame(self.labelFrame, text = "Contrast")
        self.contrastFrame.grid(column = 2, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: append
        self.buttonShow = ttk.Button(self.labelFrame, text = "Append to PDF", command = self.appendImage)
        self.buttonShow.grid(column = 3, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: save
        self.buttonShow = ttk.Button(self.labelFrame, text = "Save PDF", command = self.outputFile)
        self.buttonShow.grid(column = 4, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        # rotation
        self.rotateValue = StringVar()
        self.rotateValue.set(DEFAULT_ROTATION)
        self.spinBox = Spinbox(
            self.rotateFrame,
            from_=-180,
            to=180,
            increment=0.2,
            textvariable=self.rotateValue,
            width=6,
            command=self.rotateImage
            )
        self.spinBox.pack(padx=DEFAULT_PAD, pady=DEFAULT_PAD)

        # contrast
        self.contrastValue = StringVar()
        self.contrastValue.set(DEFAULT_CONTRAST)
        self.spinBox = Spinbox(
            self.contrastFrame,
            from_=0.0,
            to=2.0,
            increment=0.1,
            textvariable=self.contrastValue,
            width=5,
            command=self.contrastImage
            )
        self.spinBox.pack(padx=DEFAULT_PAD, pady=DEFAULT_PAD)

        # empty images
        self.whiteColor = (255, 255, 255)
        emptyImg = Image.new("RGB", (DEFAULT_INPUT_IMAGE_SIZE, DEFAULT_INPUT_IMAGE_SIZE), self.whiteColor)
        emptyPhotoImg = ImageTk.PhotoImage(emptyImg)  
        # show input
        self.canvas = Canvas(self.inputImageFrame, width=DEFAULT_INPUT_IMAGE_SIZE, height=DEFAULT_INPUT_IMAGE_SIZE)  
        self.canvas.pack()
        self.canvasImage = self.canvas.create_image(5, 5, anchor=NW, image=emptyPhotoImg) 
        self.canvas.image = emptyPhotoImg
        # show output
        self.outputCanvas = Canvas(self.outputImageFrame, width=DEFAULT_INPUT_IMAGE_SIZE, height=DEFAULT_INPUT_IMAGE_SIZE)  
        self.outputCanvas.pack()
        self.outputCanvasImage = self.outputCanvas.create_image(5, 5, anchor=NW, image=emptyPhotoImg) 
        self.outputCanvas.image = emptyPhotoImg

        # output images
        self.outputImages = []

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

    def rotateImage(self):
        self.processImage(image=self.reducedImg)

    def contrastImage(self):
        self.processImage(image=self.reducedImg)

    def appendImage(self):
        self.processImage(image=self.img, append=True)

    def outputFile(self):
        self.processImage(image=self.img, save=True)

    def processImage(self, image=None, save=False, append=False):
        # rotate
        outputImg = image.rotate(float(self.rotateValue.get()), expand=0, fillcolor=self.whiteColor)
        # contrast
        enhancer = ImageEnhance.Contrast(outputImg)
        outputImg = enhancer.enhance(float(self.contrastValue.get()))
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
            self.outputImages.append(outputImg)
        # save
        if save:
            filename = filedialog.asksaveasfilename(
                initialdir = DEFAULT_OUTPUT_PATH, 
                title = "Output File", 
                filetypes = (("document files","*.pdf"),("all files","*.*")) )
            self.outputImages[0].save(filename, save_all=True, append_images=self.outputImages[1:])
            # clear output images 
            self.outputImages = []

root = Root()
root.mainloop()
