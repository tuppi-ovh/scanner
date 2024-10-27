# Document Scanner

## Overview

The main idea of this project is to simplify the document scanning process:
- open scanned image file (done)
- rotate and apply contrast (done)
- save output as pdf file (done)

![image](images/screenshot.png)

## Requirements

*Important! The steps described below were tested with python version 3.7.*

- Execute these commands:

```sh 
# Install dependencies
sudo apt-get install python3-tk
sudo apt-get install tesseract-ocr

# Create a virtual envirenment
python3 -m venv .venv

# Install requirements
.venv/bin/python3 -m pip -r requirements.txt
```

- Define environment variable `TESSDATA_PREFIX` to `~/.tessdata/`.

- Download tesseract dictionnaries to `~/.tessdata/`.

## Configuration File

Create `config.py` in the repository with this content:

```py
DEFAULT_INPUT_PATH = "/absolut/path/to/open/input/file"
DEFAULT_OUTPUT_PATH = "/absolut/path/to/save/output/file"
```

## Quick Start Guide - GUI 

- Launch GUI: `python3 ./.venv/python3 scanner.py --gui`.

## Quick Start Guide - Console

Prepare a file in format:

```
$ output-path-1/filename-1.pdf: img_01.png img_02.png
$ output-path-2/filename-2.pdf: img_03.png
$ output-path-1/filename-3.pdf: img_04.png
```

Replace `:` by ` --input` and `$` by `.venv/bin/python3 scanner.py --pdf --output` 
to get the file in this format:

```sh
.venv/bin/python3 scanner.py --pdf --output output-path-1/filename-1.pdf --input img_01.png img_02.png
.venv/bin/python3 scanner.py --pdf --output output-path-2/filename-2.pdf --input img_03.png
.venv/bin/python3 scanner.py --pdf --output output-path-1/filename-3.pdf --input img_04.png
```

Save this file as bash script and execute it.

## Frames

```
|-------------------frame0-----------------------|
|-------frame00--------|--------frame01----------|
|-------frame000-------|                         |
|-------frame001-------|                         |         
|-------frame002-------|                         |
|-------------------frame1-----------------------|
|---frame10----|-----frame11----|----frame12-----|
|              |                |                |
|--------------|----------------|----------------|
```

## Generate Tags

```sh
$ find . -maxdepth 10 -type d -printf '%P \n' | grep -v ".git"
```

## License

Refer to the [LICENSE](LICENSE) file.

## TODO

- Preview the next file.
- Add filename pattern.