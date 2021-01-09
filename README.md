# Shopify Image Repository
Created for the Summer 2021 Shopify Developer Intern Challenge

> **NOTICE:** This project was developed using Python 3.9 in Windows 10. Although there is code specific to Mac OS X, it has **NOT** been properly tested. Therefore, there is a chance the program will quit prematurly if it is unable to install the necessary libraries. If running on Mac OS X, it is reccomended you instead follow the manual instructions outlined in [Setup](#setup).



## Table of contents
* [General Info](#general-info)
	* [Supported Formats](#supported-formats)
* [Setup](#setup)
* [Running the Project](#running-the-project)
* [Built With](#built-with)
* [Contact](#contact)

## General Info
This project is a simple image repository that allows users to upload, download, and delete images. Every user must create an account with a username and password. Once they are logged in, they can interact with photos in their personal private library or the global public library (which everyone can access).
### Supported Formats
Currently, this project supports the following image formats: `.jpg`, `.jpeg`, `.png`, and `.gif`*.

**Note: Any animated `.gif` files that are uploaded to the repository will only display a preview of the first frame. To view the entire animation in sequence, you can download the file and open it elsewhere.*
	


## Setup
If you do not have it already, download the latest version of Python [here](https://www.python.org/downloads/). You must have at least Python 3.9.0 installed to ensure the application runs as expected.

Create a folder such as `Image Repository` somewhere on your computer and place the `main.py` inside of it. *When the application is run, it will create numerous folders to organize user data within its current working directory. Thus, it is important to place the file in a brand new folder where it is free to setup its own file system.*


When `main.py` is run, it will attempt to install the necessary libraries itself using the package manager [pip](https://pip.pypa.io/en/stable/). If errors are encountered, you can try to manually install the required [Pillow](https://python-pillow.org/) library using the commands below.

### Windows
Enter the following into the command prompt:
```bash
pip install pillow
```

### Macintosh
Although it is recommended to use Window 10 as that was the environment used for testing, the steps below can be followed to manually install [Pillow](https://python-pillow.org/) on Mac OS X.

First, enter the following into the terminal:
```bash
pip install pillow
```

If an error is encountered, your computer may be defaulting to Python 2 (which is automatically installed with OS X) as opposed to Python 3. To avoid this, enter the command below into the terminal:
```bash
pip3 install pillow
```



## Running the Project
To run the project, navigate to the location where `main.py` is stored and run the following commands that correspond with your operating system.

### Windows
Enter the following into the command prompt:
```bash
python main.py
```

### Macintosh
First, try entering the following into the terminal:
```bash
python main.py
```

If the above command fails, try with this one instead.
```bash
python3 main.py
```



## Built With
This project uses:
* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [Pillow](https://python-pillow.org/)


## Author
Cameron Estabrooks

Project Link: https://github.com/cestabrooks/Shopify-Image-Repository
