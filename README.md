# Shopify Image Repository
Created for the Summer 2021 Shopify Developer Intern Challenge

## Table of contents
* [General Info](#general-info)
	* [Supported Formats](#supported-formats)
* [Setup](#setup)
* [Running the Project](#running-the-project)
* [Built With](#built-with)
* [Contact](#contact)

## General Info
This project is a simple image repository that allows users to upload, download, and delete images. Every user must create an account with a username and password. Once they are logged in, they can interact with photos in their personal private libaray or the global public libary (which everyone can access).
### Supported Formats
Currently, this project supports the following image formats: `.jpg`, `.jpeg`, `.png`, and `.gif`*.

**Note: Any animated `.gif` files that are uploaded to the repository will only display a preview of the first frame. To view the entire animation in sequence, you can download the file and open it elsewhere.*
	
	
## Setup
Create a folder such as `Image Repository` somewhere on your computer and place the `main.py` inside of it. *When the application is run, it will create numerous folders to organize user data within its current working directory. Thus, it is important to place the file in a brand new folder where it is free to create its own file system.*


When `main.py` is run, it will attempt to install the necessary libraries itself using the package manager [pip](https://pip.pypa.io/en/stable/). If errors are encoutered, you can try manually install the required [Pillow](https://python-pillow.org/) library with the following command.
```bash
pip install pillow
```


## Running the Project
To run the project, navigate to the location where `main.py` is stored and run the following command.
```bash
python main.py
```


## Built With
This project uses:
* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [Pillow](https://python-pillow.org/)


## Author
Cameron Estabrooks

Project Link: https://github.com/cestabrooks/Shopify-Image-Repository
