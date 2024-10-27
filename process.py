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

from PIL import ImageTk, Image, ImageEnhance

import config

DEFAULT_FILENAME = ""
DEFAULT_CONTRAST = 200
DEFAULT_ROTATION = 0.0
DEFAULT_CROP_X_LEFT = 1
DEFAULT_CROP_X_RIGHT = 100
DEFAULT_CROP_Y_TOP = 0
DEFAULT_CROP_Y_BOTTOM = 100
DEFAULT_INPUT_IMAGE_SIZE = 400

class ScannerProcess():

    def __init__(self):
        # public
        self.whiteColor = (255, 255, 255)
        # protected
        self._cropLeft   = DEFAULT_CROP_X_LEFT   # float(self.cropLeftValue.get())
        self._cropRight  = DEFAULT_CROP_X_RIGHT  # float(self.cropRightValue.get())
        self._cropTop    = DEFAULT_CROP_Y_TOP    # float(self.cropTopValue.get()) 
        self._cropBottom = DEFAULT_CROP_Y_BOTTOM # float(self.cropBottomValue.get())
        self._rotation = DEFAULT_ROTATION # float(self.rotateValue.get())
        self._contrast = DEFAULT_CONTRAST # float(self.contrastValue.get())
        self._outputImages = []
        self._outputImagesFiles = []

    def processImage(self, image=None, filename=None, savePdf=None, append=False):
        # rotate
        outputImg = image.rotate(self._rotation, expand=0, fillcolor=self.whiteColor)
        # contrast
        enhancer = ImageEnhance.Contrast(outputImg)
        outputImg = enhancer.enhance(self._contrast * 0.01)
        # crop 
        width, height = outputImg.size
        left = width * self._cropLeft * 0.01
        top = height * self._cropTop * 0.01
        right = width * self._cropRight * 0.01
        bottom = height * self._cropBottom * 0.01
        outputImg = outputImg.crop((left, top, right, bottom)) 
        # append 
        if append:
            if outputImg.mode == 'RGBA':
                outputImg = outputImg.convert('RGB')
            self._outputImages.append(outputImg)
            self._outputImagesFiles.append(filename)
        # save
        if savePdf is not None:
            self._outputImages[0].save(savePdf, save_all=True, append_images=self._outputImages[1:])
            # move input files
            for filename in self._outputImagesFiles:
                os.rename(filename, f"{config.DEFAULT_TRASH_PATH}/{os.path.basename(filename)}")
            # clear everything
            self._outputImages = []
            self._outputImagesFiles = []
        # output image
        return outputImg