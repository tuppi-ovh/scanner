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

import argparse

from PIL import Image

import config
import gui
import process

def main():
    """ Entry point function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Input filename list.", required=False, default=None, nargs='+')
    parser.add_argument("--output", help="Output filename.", required=False, default=None)
    parser.add_argument("--pdf", help="Save output as PDF.", action="store_true")
    parser.add_argument("--gui", help="Launch GUI.", action="store_true")
    args = parser.parse_args()

    # GUI mode
    if args.gui:
        gui.guiRun()
    # command line
    elif args.pdf:
        # process
        if args.input is not None:
            scanner = process.ScannerProcess()

            for i in range(len(args.input)):
                image = Image.open(f"{config.DEFAULT_INPUT_PATH}/{args.input[i]}")
                # define save_pdf parameter 
                if i < (len(args.input)-1):
                    save_pdf = None
                elif args.output is not None:
                    save_pdf = f"{config.DEFAULT_OUTPUT_PATH}/{args.output}"
                else:
                    save_pdf = f"{config.DEFAULT_OUTPUT_PATH}/{args.input}.pdf"
                # process
                scanner.process_image(
                    image=image, 
                    filename=f"{config.DEFAULT_INPUT_PATH}/{args.input[i]}",
                    save_pdf=save_pdf,
                    append=True
                )
        else:
            print("Define --input parameter.")

if __name__ == "__main__":
    main()
