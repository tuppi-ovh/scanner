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

import gui

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--counter", help="COUCOU.", required=False, type=int)
    parser.add_argument("--gui", help="Launch GUI.", action="store_true")
    args = parser.parse_args()
    
    if args.gui:
        gui.guiRun()

if __name__ == "__main__":
    main()
