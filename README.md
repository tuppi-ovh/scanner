# Document Scanner

## Overview

The main idea of this project is to simplify the document scanning process:
- open scanned image file (done)
- rotate and apply contrast (done)
- save output as pdf file (done)

![image](images/screenshot.png)

## Requirements

*Important! The steps described below were tested with python version 3.7.*

Execute these commands:

```sh 
# Create a virtual envirenment
python3 -m venv venv

# Enter in virtual envirenment
source venv/bin/activate

# Install dependencies
sudo apt-get install python3-tk
python3 -m pip install pillow
python3 -m pip install pytesseract
```

## Configuration File

Create `config.py` in the repository with this content:

```py
DEFAULT_INPUT_PATH = "/absolut/path/to/open/input/file"
DEFAULT_OUTPUT_PATH = "/absolut/path/to/save/output/file"
```

## Launch

Execute these commands:

```sh 
# Enter in virtual envirenment
source venv/bin/activate

## Launch GUI
python3 gui.py
```

## License

Refer to the [LICENSE](LICENSE) file.
