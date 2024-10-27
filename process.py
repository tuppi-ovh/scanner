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

from PIL import ImageEnhance

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
    """ Class defining scanner process methods. 
    """

    def __init__(self):
        """ Constructor.
        """
        # public
        self.white_color = (255, 255, 255)
        # protected
        self._crop_left   = DEFAULT_CROP_X_LEFT
        self._crop_right  = DEFAULT_CROP_X_RIGHT
        self._crop_top    = DEFAULT_CROP_Y_TOP
        self._crop_bottom = DEFAULT_CROP_Y_BOTTOM
        self._rotation = DEFAULT_ROTATION
        self._contrast = DEFAULT_CONTRAST
        self._images = []
        self._images_files = []

    def set_params(self, 
                    crop_x=(DEFAULT_CROP_X_LEFT,DEFAULT_CROP_X_RIGHT), 
                    crop_y=(DEFAULT_CROP_Y_TOP,DEFAULT_CROP_X_RIGHT), 
                    rotation=DEFAULT_ROTATION, contrast=DEFAULT_CONTRAST):
        """ Set process parameters.
        """
        self._crop_left, self._crop_right = crop_x
        self._crop_top, self._crop_bottom = crop_y
        self._rotation = rotation
        self._contrast = contrast

    def process_image(self, image=None, filename=None, save_pdf=None, append=False):
        """ Process image and return resulting image.
        """
        # rotate
        img_out = image.rotate(self._rotation, expand=0, fillcolor=self.white_color)
        # contrast
        enhancer = ImageEnhance.Contrast(img_out)
        img_out = enhancer.enhance(self._contrast * 0.01)
        # crop
        width, height = img_out.size
        left = width * self._crop_left * 0.01
        top = height * self._crop_top * 0.01
        right = width * self._crop_right * 0.01
        bottom = height * self._crop_bottom * 0.01
        img_out = img_out.crop((left, top, right, bottom))
        # append
        if append:
            if img_out.mode == 'RGBA':
                img_out = img_out.convert('RGB')
            self._images.append(img_out)
            self._images_files.append(filename)
        # save
        if save_pdf is not None:
            self._images[0].save(save_pdf, save_all=True, append_images=self._images[1:])
            # move input files
            for f in self._images_files:
                os.rename(f, f"{config.DEFAULT_TRASH_PATH}/{os.path.basename(f)}")
            # clear everything
            self._images = []
            self._images_files = []
        # output image
        return img_out
