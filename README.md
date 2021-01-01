# Document Scanner

The main idea of this project is to simplify the document scanning procedure:
- scan using the physical scanner (maybe comming soon)
- rotate, resize and apply contrast (done using `OpenCV-Document-Scanner` project)
- save output as pdf file (maybe comming soon)

# Prepare Repository

*Important! The steps described below were tested with python version 3.7.*

Execute these commands:
```sh 
# Clone external projects
git clone https://github.com/joaofauvel/OpenCV-Document-Scanner.git

# Create a virtual envirenment
python3 -m venv venv

# Enter in virtual envirenment
source venv/bin/activate

# Install dependencies
sudo apt-get install python3-tk
python3 -m pip install -r requirements.txt

# Make sure you have output directory
mkdir output
```

# Execution 

```sh
python3 OpenCV-Document-Scanner/scan.py --image perso/test.png -i
```

# License

Refer to the [LICENSE](LICENSE) file.