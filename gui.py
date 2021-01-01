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

For information on Data Server PI: tuppi.ovh@gmail.com
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk,Image 

from OpenCV_Document_Scanner import scan

DEFAULT_INPUT_PATH = "/mnt/c/__DATA__/GIT/tuppi-ovh/scanner/perso"
DEFAULT_INPUT_IMAGE_SIZE = 300

DEFAULT_OUTPUT_FILENAME = "/mnt/c/__DATA__/GIT/tuppi-ovh/scanner/output/temp.png"


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)
 
        self.labelFrame = ttk.LabelFrame(self, text = "Commands")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
    
        self.inputImageFrame = ttk.LabelFrame(self, text = "Input File")
        self.inputImageFrame.grid(column = 0, row = 2, padx = 20, pady = 20)
    
        self.outputImageFrame = ttk.LabelFrame(self, text = "Output File")
        self.outputImageFrame.grid(column = 2, row = 2, padx = 20, pady = 20)
        
        self.button = ttk.Button(self.labelFrame, text = "Browse Input File", command = self.fileDialog)
        self.button.grid(column = 0, row = 1)

        self.button = ttk.Button(self.labelFrame, text = "Process", command = self.processImage)
        self.button.grid(column = 1, row = 3)
 
    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir = DEFALT_INPUT_PATH, title = "Select A File", filetypes =
        (("image files","*.png"),("all files","*.*")) )
        # image 
        self.img = Image.open(self.filename)
        width, height = self.img.size
        ratio = min(DEFALT_INPUT_IMAGE_SIZE / width, DEFALT_INPUT_IMAGE_SIZE / height)
        self.img = self.img.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)  
        # show
        self.canvas = Canvas(self.inputImageFrame, width = DEFALT_INPUT_IMAGE_SIZE, height = DEFALT_INPUT_IMAGE_SIZE)  
        self.canvas.pack()
        self.canvas.create_image(5, 5, anchor=NW, image=self.img) 
        self.canvas.image = self.img  

    def processImage(self):
        # scan
        scanner = scan.DocScanner(True)
        scanner.scan(self.filename)
        # image 
        self.outputImg = Image.open(DEFAULT_OUTPUT_FILENAME)
        width, height = self.outputImg.size
        ratio = min(DEFALT_INPUT_IMAGE_SIZE / width, DEFALT_INPUT_IMAGE_SIZE / height)
        self.outputImg = self.outputImg.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
        self.outputImg = ImageTk.PhotoImage(self.img)  
        # show
        self.outputCanvas = Canvas(self.outputImageFrame, width = DEFALT_INPUT_IMAGE_SIZE, height = DEFALT_INPUT_IMAGE_SIZE)  
        self.outputCanvas.pack()
        self.outputCanvas.create_image(5, 5, anchor=NW, image=self.outputImg) 
        self.outputCanvas.image = self.outputImg  
 
root = Root()
root.mainloop()