"""
Document Scanner - Simplify the document scanning process.
Copyright (C) 2021-2024 tuppi-ovh

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
import pytesseract

#from tkinter import *
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import Listbox, StringVar, Spinbox
from tkinter import Canvas
from tkinter import CENTER, END
from PIL import ImageTk, Image, ImageEnhance

import config
import process

CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

DEFAULT_INPUT_IMAGE_SIZE = process.DEFAULT_INPUT_IMAGE_SIZE

DEFAULT_PAD = 5
DEFAULT_TAGS = ""

def reduceFilename(filename):
    length = len(filename)
    max_length = 40
    if length > max_length:
        filename = "..." + filename[(length - max_length):]
    return filename

class Root(Tk):
    def __init__(self):
        # protected vars
        self._scannerProcess = process.ScannerProcess()
        # public vars
        self.img = None
        self.reducedImg = None
        self.filename = None
        self.outputImages = []
        self.outputImagesFiles = []
        self.logCounter = 0
        # init
        super(Root, self).__init__()
        self.buildGui()
        self.buildTags()
        

    def buildGuiCrop(self, frame, column_from, row, text, cmd, from_, to_):
        # crop label
        label = ttk.Label(frame, text=text)
        label.grid(column = column_from, row = row, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # crop spinbox
        value = StringVar()
        value.set(from_)
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
        value2.set(to_)
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
        self.frame0 = ttk.Frame(self)
        self.frame0.grid(column = 0, row = 0)
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column = 0, row = 1)

        self.frame00 = ttk.Frame(self.frame0)
        self.frame00.grid(column = 0, row = 0)
        self.frame01 = ttk.Frame(self.frame0)
        self.frame01.grid(column = 1, row = 0)

        self.frame000 = ttk.Frame(self.frame00)
        self.frame000.grid(column = 0, row = 0)
        self.frame001 = ttk.Frame(self.frame00)
        self.frame001.grid(column = 0, row = 1)
        self.frame002 = ttk.Frame(self.frame00)
        self.frame002.grid(column = 0, row = 2)

        self.frame10 = ttk.LabelFrame(self.frame1, text = "Input Image")
        self.frame10.grid(column = 0, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
    
        self.frame11 = ttk.LabelFrame(self.frame1, text = "Output Image")
        self.frame11.grid(column = 1, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD) 

        self.frame12 = ttk.LabelFrame(self.frame1, text = "Parsed Text")
        self.frame12.grid(column = 2, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD) 

        # Commands: button open image
        self.buttonInput = ttk.Button(self.frame000, text = "Open Image", command = self.openFile)
        self.buttonInput.grid(column = 0, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: button parse image
        self.buttonParseImage = ttk.Button(self.frame000, text = "Parse Image", command = self.parseImage)
        self.buttonParseImage.grid(column = 1, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: append
        self.buttonShow = ttk.Button(self.frame000, text = "Append to PDF", command = self.appendImage)
        self.buttonShow.grid(column = 2, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: button parse tags
        self.buttonParseTags = ttk.Button(self.frame000, text = "Parse Tags", command = self.parseTags)
        self.buttonParseTags.grid(column = 3, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Commands: save
        self.buttonShow = ttk.Button(self.frame000, text = "Save PDF", command = self.outputFile)
        self.buttonShow.grid(column = 4, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        # rotation label
        self.rotateLabel = ttk.Label(self.frame001, text = "Rotation:")
        self.rotateLabel.grid(column = 0, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # rotation spinbox
        self.rotateValue = StringVar()
        self.rotateValue.set(process.DEFAULT_ROTATION)
        self.rotateSpinBox = Spinbox(
            self.frame001,
            from_=-180,
            to=180,
            increment=0.2,
            textvariable=self.rotateValue,
            width=6,
            command=self.rotateImage
            )
        self.rotateSpinBox.grid(column = 1, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # contrast label
        self.contrastLabel = ttk.Label(self.frame001, text = "Contrast:")
        self.contrastLabel.grid(column = 2, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # contrast spinbox
        self.contrastValue = StringVar()
        self.contrastValue.set(process.DEFAULT_CONTRAST)
        self.contrastSpinBox = Spinbox(
            self.frame001,
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
            frame = self.frame001,
            column_from = 0,
            row = 1,
            text = "Crop on X:",
            cmd = self.cropImage,
            from_ = process.DEFAULT_CROP_X_LEFT,
            to_ = process.DEFAULT_CROP_X_RIGHT
            )
        # crop y
        self.cropTopValue, self.cropBottomValue = self.buildGuiCrop(
            frame = self.frame001,
            column_from = 3,
            row = 1,
            text = "Crop on Y:",
            cmd = self.cropImage,
            from_ = process.DEFAULT_CROP_Y_TOP,
            to_ = process.DEFAULT_CROP_Y_BOTTOM
            )
        # Tags label
        self.tagsLabel = ttk.Label(self.frame002, text = "Tags:")
        self.tagsLabel.grid(column = 0, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Tags entry
        self.tagsValue = StringVar()
        self.tagsValue.set(DEFAULT_TAGS)
        self.tagsEntry = ttk.Entry(
            self.frame002,
            textvariable=self.tagsValue,
            width=80
            )
        self.tagsEntry.grid(column = 1, row = 2, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Filename label
        self.filenameLabel = ttk.Label(self.frame002, text = "Fiename:")
        self.filenameLabel.grid(column = 0, row = 3, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # Filename entry
        self.filenameValue = StringVar()
        self.filenameValue.set(process.DEFAULT_FILENAME)
        self.filenameEntry = ttk.Entry(
            self.frame002,
            textvariable=self.filenameValue,
            width=80
            )
        self.filenameEntry.grid(column = 1, row = 3, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        # log listbox
        self.logList = Listbox(self.frame01, height=6, width=70)
        self.logList.grid(column = 1, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        # parse listbox
        self.parseList = Listbox(self.frame12, height=25, width=70)
        self.parseList.grid(column = 1, row = 0, padx = DEFAULT_PAD, pady = DEFAULT_PAD)

        # empty images
        emptyImg = Image.new("RGB", (DEFAULT_INPUT_IMAGE_SIZE, DEFAULT_INPUT_IMAGE_SIZE), self._scannerProcess.white_color)
        emptyPhotoImg = ImageTk.PhotoImage(emptyImg)  
        # show input
        self.canvas = Canvas(self.frame10, width=DEFAULT_INPUT_IMAGE_SIZE, height=DEFAULT_INPUT_IMAGE_SIZE)  
        self.canvas.pack()
        self.canvasImage = self.canvas.create_image(DEFAULT_INPUT_IMAGE_SIZE/2, DEFAULT_INPUT_IMAGE_SIZE/2, anchor=CENTER, image=emptyPhotoImg) 
        self.canvas.image = emptyPhotoImg
        # show output
        self.outputCanvas = Canvas(self.frame11, width=DEFAULT_INPUT_IMAGE_SIZE, height=DEFAULT_INPUT_IMAGE_SIZE)  
        self.outputCanvas.pack()
        self.outputCanvasImage = self.outputCanvas.create_image(DEFAULT_INPUT_IMAGE_SIZE/2, DEFAULT_INPUT_IMAGE_SIZE/2, anchor=CENTER, image=emptyPhotoImg) 
        self.outputCanvas.image = emptyPhotoImg

    def listdirs(self, rootdir, dirs):
        """ List directories and subdirectories.
        """
        for it in os.scandir(rootdir):
            if it.is_dir():
                if '.git' not in it.path:
                    dirs.append(os.path.abspath(it.path))
                    self.listdirs(it, dirs)

    def buildTags(self):
        """ Build tags by scanning all directories.
        """
        dirs = []
        self.tags = {}
        self.listdirs(config.DEFAULT_OUTPUT_PATH, dirs)
        output_path = os.path.abspath(config.DEFAULT_OUTPUT_PATH)
        for d in dirs:
            d = d.replace(output_path +"/", "")  # unix
            d = d.replace(output_path +"\\", "") # windows
            key = d
            d = d.lower()
            d = d.replace("/", " ")  # unix
            d = d.replace("\\", " ") # windows
            d = d.replace("-", " ")
            tags = d.split(" ")
            self.tags[key] = tags
            #print(f"{key}: {tags}")
        
    def log(self, message):
        self.logList.insert(0, " [{}] {}".format(self.logCounter, message))
        self.logCounter += 1

    def openFile(self):
        self.filename = filedialog.askopenfilename(
            initialdir=config.DEFAULT_INPUT_PATH, 
            title="Input File", 
            filetypes=(("image files","*.png"),("all files","*.*")) 
            )
        # scale
        self.img = Image.open(self.filename)
        width, height = self.img.size
        ratio = min(DEFAULT_INPUT_IMAGE_SIZE / width, DEFAULT_INPUT_IMAGE_SIZE / height)
        self.reducedImg = self.img.resize((int(width * ratio), int(height * ratio)), Image.LANCZOS)
        inputPhotoImg = ImageTk.PhotoImage(self.reducedImg)
        # default values
        self.rotateValue.set(process.DEFAULT_ROTATION)
        self.contrastValue.set(process.DEFAULT_CONTRAST)
        # show input
        self.canvas.itemconfig(self.canvasImage, image = inputPhotoImg)
        self.canvas.image = inputPhotoImg
        # process output
        self.processImage(image=self.reducedImg)
        # log
        self.log("Open file {}".format(reduceFilename(self.filename)))

    def parseImage(self):
        """ Parse image and print the text 
        """
        pytesseract.tesseract_cmd = "tesseract" 
        text = pytesseract.image_to_string(self.img)
        lines = text[:-1].split("\n")
        for l in lines:
            self.parseList.insert(END, l)

    def parseTags(self):
        """ Search tags in the database.
        """
        input_tags = self.tagsValue.get().split(" ")
        score_max = 0
        for key, value in self.tags.items():
            score = 0
            for tag in input_tags:
                if tag in value:
                    score = score + 1
            if score > score_max:
                score_max = score
                self.filenameValue.set(key)
        score_percent = score_max/len(input_tags)*100
        self.log(f"Parse tags with score {int(score_percent)} %")

    def rotateImage(self):
        self.processImage(image=self.reducedImg)

    def contrastImage(self):
        self.processImage(image=self.reducedImg)

    def cropImage(self):
        self.processImage(image=self.reducedImg)

    def appendImage(self):
        self.processImage(image=self.img, filename=self.filename, append=True)
        # log
        self.log("Append file {} to PDF ({})".format(reduceFilename(self.filename), len(self.outputImages)))

    def outputFile(self):
        self.filenamePdf = f"{config.DEFAULT_OUTPUT_PATH}/{self.filenameValue.get()}"
        # process command
        self.processImage(image=self.img, save_pdf=self.filenamePdf)
        # log
        self.log("Save PDF as {}".format(reduceFilename(self.filenamePdf)))
        self.log("------------------------------")

    def processImage(self, image=None, filename=None, save_pdf=None, append=False):
        # process params
        self._scannerProcess.set_params(
            crop_x=(float(self.cropLeftValue.get()),float(self.cropRightValue.get())),
            crop_y=(float(self.cropTopValue.get()),float(self.cropBottomValue.get())),
            rotation=float(self.rotateValue.get()), 
            contrast=float(self.contrastValue.get())
        )
        # process image
        output = self._scannerProcess.process_image(
            image=image, 
            filename=filename, 
            save_pdf=save_pdf, 
            append=append
        )
        # update output
        self.updateOutputCanvas(img=output)
        # reset
        self.parseList.delete(0, END)
        self.tagsValue.set("")
        self.filenameValue.set("")

    def updateOutputCanvas(self, img):
        width, height = img.size
        ratio = min(DEFAULT_INPUT_IMAGE_SIZE / width, DEFAULT_INPUT_IMAGE_SIZE / height)
        outputPhotoImg = img.resize((int(width * ratio), int(height * ratio)), Image.LANCZOS)
        outputPhotoImg = ImageTk.PhotoImage(outputPhotoImg)
        # show output
        self.outputCanvas.itemconfig(self.outputCanvasImage, image = outputPhotoImg)
        self.outputCanvas.image = outputPhotoImg

def guiRun():
    root = Root()
    root.mainloop()
