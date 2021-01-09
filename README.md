# Shopify Image Repository
Created for the Summer 2021 Shopify Developer Intern Challenge

> **NOTICE:** This project was developed using Python 3.9 in Windows 10. Although there is code specific to Mac OS X, it has **not** been properly tested.


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
If you do not have it already, download the latest version of Python [here](https://www.python.org/downloads/) (you must have at least Python 3.9.0 installed).

Create a folder such as `Image Repository` somewhere on your computer and place the `main.py` inside of it. *When the application is run, it will create numerous folders to organize user data within its current working directory. Thus, it is important to place the file in a brand new folder where it is free to create its own file system.*


When `main.py` is run, it will attempt to install the necessary libraries itself using the package manager [pip](https://pip.pypa.io/en/stable/). If errors are encountered, you can try to manually install the required [Pillow](https://python-pillow.org/) library with the following command:
```bash
pip install pillow
```

If you are using Mac OS X and errors still arise, your computer may be using Python 2 (which is automatically installed with OS X) as opposed to Python 3. Instead, try installing [Pillow](https://python-pillow.org/) with the following command:
```bash
pip3 install pillow
```


## Running the Project
To run the project, navigate to the location where `main.py` is stored and run the following command.
```bash
python main.py
```

If you are using Mac OS X and errors arise when using the command above, your computer may be using Python 2 (which is automatically installed with OS X) as opposed to Python 3. Instead, try using the following command:
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
