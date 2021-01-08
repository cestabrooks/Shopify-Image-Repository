# IMAGE REPOSITORY
# Author: Cameron Estabrooks
# Current Version: 1.0
#
#
# Version History:
#   v1.0    Janurary 7, 2020
#


# Importing reuired libraries
import sys
import enum
import shutil
import os
import platform
import webbrowser


# Trying to import tkinter (needed for GUI)
try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter import filedialog
except:
    print("ERROR: Unable to access 'tkinter' library. This library is required to run the GUI for this application.\n")
    sys.exit()


# Trying to import pillow library (needed to display images)
try:
    #import Image
    from PIL import Image, ImageTk
# If unsuccesful, try to install pillow
except:
    print("ERROR: You are missing the libraries required to display images.\n")
    print("Attempting to install 'pillow' now!")

    # Installation commands depending on the operating system (Note: "Darwin" means Mac OSX)
    if platform.system() == 'Darwin':
        os.system("sudo easy_install pip")
        os.system("pip install pillow")
    elif platform.system() == 'Windows':
        os.system("pip install pillow")

    # Now, try to install again
    try:
        from PIL import Image, ImageTk
        print("Install successful! Beginning program...")
    except:
        print("ERROR: Install unsuccessful! Unable to install 'pillow' on this device.")
        sys.exit()



# Store the current directory that the application script is running from
topLevelDir = os.getcwd()

# Make this true if you want to debug
# **NOTE: THIS WILL PRINT SENSTIVE INFO INCLUDING:
#   - All user's usernames and passwords
#   - Names of image files for a given user
debug = False

# Store default values for colours
bgColour = "gray12"         # Backgroun colour
txtColour = "white"         # Text colour

butColour = "gray20"        # Button background colour
butTxtColour = "gray60"     # Button text colout


# Enumerated list for returning whether a function/method was successful (SUCCESS) or unsuccessful (ERROR)
class ExitCode(enum.Enum):
    SUCCESS = 0
    ERROR = 1

# Enumerated list for the type of image albums available
class AlbumView(enum.Enum):
    PRIVATE = 0     # User's private album (only current user can contribute)
    PUBLIC = 1      # Global public album (everyone can contribute)




# Class for the graphical user interface of the image repository
class ImgRepGUI:
    # Inital setup
    def __init__(self, database):
        self.databaseOfUsers = database         # Stores references to the database that the application will use

        self.currentUser = None                 # Stores the current user at any time    
        self.currentAlbum = None                # Stores the current album type that is being viewed (private or public)
        self.currentImage = None                # Stores reference to the currently selected image that is being displayed*
        self.imgListBoxWidget = None            # Stores reference to the image selection list box widget (needed for using "Select All")

        self.listOfPriorSelections = []         # Stores list of all selected images (nessecary to determine current selection)

        #   * This is required since garbage collection on Tkinter would get rid of 
        #     any local image references within a function or method after it has
        #     been called. Therefore, we need to store a reference to that image
        #     for as long as we need it displayed.


        # Setting up the main window
        self.mainWindow = Tk()
        self.mainWindow.title("Image Repository")
        self.mainWindow.geometry("600x400")
        self.mainWindow.minsize(600,400)
        self.mainWindow.configure(bg=bgColour)


        # Setting up the menu bar system with all of its menu button options
        self.menuBar = Menu(self.mainWindow)
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.editMenu = Menu(self.menuBar, tearoff=0)
        self.viewMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.CreateMenu()

        # Setting up title text to be displayed on main window
        self.title = Label(self.mainWindow, text="Image Repository", font=("Verdana Bold", 25), fg=txtColour, bg=bgColour)
        self.title.pack(padx=10, pady=(30,0))

        # Setting the current frame to the starting login frame
        self.currentFrame = self.StartFrame()
    

    # Starts the application
    def Run(self):
        self.mainWindow.mainloop()


    # Sets up the menu bar system
    def CreateMenu(self):
        # Setting up "File" menu button with options to upload/download photos, logout, and exit
        self.fileMenu.add_command(label="Upload Photo(s)", command=self.Upload)
        self.fileMenu.add_command(label="Download Photo(s)", command=lambda:self.SwitchFrame(self.HomeFrame(self.currentAlbum, "download")))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Log Out", command=lambda:self.SwitchFrame(self.StartFrame()))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=sys.exit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        # Setting up "Edit" menu with option to delete photos
        self.editMenu.add_command(label="Delete Photo(s)", command=lambda:self.SwitchFrame(self.HomeFrame(self.currentAlbum, "delete")))
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Select All", state=DISABLED, command=self.SelectAll)
        self.menuBar.add_cascade(label="Edit", menu=self.editMenu)

        # Setting up "View" menu button with options to view public or private photos
        self.viewMenu.add_command(label="View Your Photos", command=lambda:self.SwitchFrame(self.HomeFrame(AlbumView.PRIVATE)))
        self.viewMenu.add_command(label="View Public Photos", command=lambda:self.SwitchFrame(self.HomeFrame(AlbumView.PUBLIC)))
        self.menuBar.add_cascade(label="View", menu=self.viewMenu)

        # Setting up "Help" menu button with options to see documentation to get help and to get info about author
        self.helpMenu.add_command(label="Get Help", command=lambda:webbrowser.open("https://github.com/cestabrooks/Shopify-Image-Repository/blob/main/README.md"))
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="About", command=lambda:webbrowser.open("https://github.com/cestabrooks"))
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)


    # Activates and shows menu bar in the main window.
    def ShowMenuBar(self, showOrHide, editMode = None):
        # If showOrHide is 'False', menu bar is hidden. 
        if showOrHide == False:
            emptyMenu = Menu(self.mainWindow)
            self.mainWindow.config(menu=emptyMenu)
        # If showOrHide is 'True', menu bar is displayed.
        elif showOrHide == True:
            if editMode == "edit":
                self.editMenu.entryconfig("Select All", state=NORMAL)
                self.mainWindow.config(menu=self.menuBar)
            else:
                self.editMenu.entryconfig("Select All", state=DISABLED)
                self.mainWindow.config(menu=self.menuBar)


    # Switches from the current frame to the requeted next frame
    def SwitchFrame(self, nextFrame):
        # Destroying old frame ("currentFrame") and pack up the new one to be displayed ("nextFrame")
        self.currentFrame.destroy()
        nextFrame.pack

        #Change the current frame to the one we just switched to
        self.currentFrame = nextFrame
    

    # Starting login frame
    def StartFrame(self):
        # Hide menu bar
        self.ShowMenuBar(False)

        # Frame to hold everything beneath the title
        frame = Frame(self.mainWindow, bg=bgColour)

        # Login button
        loginBut = Button(frame, text="Login", font=("Verdana Bold", 14), fg=butTxtColour, bg=butColour, command=lambda:self.SwitchFrame(self.LoginFrame()))
        loginBut.pack(pady=20)

        # Create account button
        createAccBut = Button(frame, text="Create Account", font=("Verdana Bold", 10), fg=butTxtColour, bg=butColour, command=lambda:self.SwitchFrame(self.CreateUserFrame()))
        createAccBut.pack(pady=20)

        # Pack the frame
        frame.pack(pady=80)

        # Must always return the frame
        return frame

    
    # Existing user login frame
    def LoginFrame(self):
        self.ShowMenuBar(False)

        frame = Frame(self.mainWindow, bg=bgColour)

        frameUsername = Frame(frame, bg=bgColour)
        framePassword = Frame(frame, bg=bgColour)
        frameBut = Frame(frame, bg=bgColour)

        usernameLabel = Label(frameUsername, text="Username: ", fg=butTxtColour, bg=butColour, width=10, anchor=E)
        usernameEntry = Entry(frameUsername)
        usernameLabel.pack(side=LEFT)
        usernameEntry.pack(side=RIGHT)

        passwordLabel = Label(framePassword, text="Password: ", fg=butTxtColour, bg=butColour, width=10, anchor=E)
        passwordEntry = Entry(framePassword, show='*')
        passwordLabel.pack(side=LEFT)
        passwordEntry.pack(side=RIGHT)
        

        def dialog():
            username = (usernameEntry.get()).upper()
            password = passwordEntry.get()

            userLogin = self.databaseOfUsers.ValidateUser(username, password)
            if userLogin == ExitCode.SUCCESS:
                self.currentUser = username
                self.SwitchFrame(self.HomeFrame(AlbumView.PRIVATE))
            else:
                messagebox.showerror("Attention: Invalid Combination", "Incorrect username and password combination!\n\nNote: Passwords are case-sensitive.")

        submitBut = Button(frameBut, text="SUBMIT", font=("Verdana", 10), fg=butTxtColour, bg=butColour, command=dialog)
        submitBut.pack(pady=20)

        backBut = Button(frameBut, text="Back", font=("Verdana", 10), fg=butTxtColour, bg=bgColour, command=lambda:self.SwitchFrame(self.StartFrame()))
        backBut.pack(pady=10)

        frameUsername.pack()
        framePassword.pack()
        frameBut.pack()

        frame.pack(pady=85)

        return frame


    # New user account creation frame
    def CreateUserFrame(self):
        # Hide menu bar
        self.ShowMenuBar(False)

        # Frame to store everything beneath the titl
        frame = Frame(self.mainWindow, bg=bgColour)

        # Frames to store various sections (makes it easier to order things properly using the .pack() function)
        frameUsername = Frame(frame, bg=bgColour)
        framePassword = Frame(frame, bg=bgColour)
        framePasswordConfirm = Frame(frame, bg=bgColour)
        frameBut = Frame(frame, bg=bgColour)

        # New username entry section
        usernameLabel = Label(frameUsername, text="Create Username: ", fg=butTxtColour, bg=butColour, width=16, anchor=E)
        usernameEntry = Entry(frameUsername)
        usernameLabel.pack(side=LEFT)
        usernameEntry.pack(side=RIGHT)

        # New password entry section
        passwordLabel = Label(framePassword, text="Create Password: ", fg=butTxtColour, bg=butColour, width=16, anchor=E)
        passwordEntry = Entry(framePassword, show='*')
        passwordLabel.pack(side=LEFT)
        passwordEntry.pack(side=RIGHT)

        # New password confirm section
        passwordConfirmLabel = Label(framePasswordConfirm, text="Confirm Password: ", fg=butTxtColour, bg=butColour, width=16, anchor=E)
        passwordConfirmEntry = Entry(framePasswordConfirm, show='*')
        passwordConfirmLabel.pack(side=LEFT)
        passwordConfirmEntry.pack(side=RIGHT)
        
        # Submit button to confirm new user creation
        submitBut = Button(frameBut, text="CREATE", font=("Verdana", 10), fg=butTxtColour, bg=butColour, command=lambda:self.CreateUser(usernameEntry.get(), passwordEntry.get(), passwordConfirmEntry.get()))
        submitBut.pack(pady=20)

        # Back button to return to start screen
        backBut = Button(frameBut, text="Back", font=("Verdana", 10), fg=butTxtColour, bg=bgColour, command=lambda:self.SwitchFrame(self.StartFrame()))
        backBut.pack(pady=10)

        # Packing all the frames with "frame"
        frameUsername.pack(pady=15)
        framePassword.pack()
        framePasswordConfirm.pack()
        frameBut.pack()

        # Packing the main "frame" which sits beneath the main title
        frame.pack(pady=60)

        return frame


    # Home frame of the application where the user can view and edit their photos. Defaults to "view" mode,
    # but it can be in "delete" or "download" mode.
    def HomeFrame(self, privOrPublic : AlbumView, mode="view"):
        # Show proper menu bar
        if mode == "view":
            self.ShowMenuBar(True) 
        else:
            self.ShowMenuBar(True, "edit")

        # Updating the global object variables
        self.currentAlbum = privOrPublic

        # Resetting the global object variables
        self.currentImage = None
        self.listOfPriorSelections = []
        self.imgListBoxWidget = None


        # Setting up frame
        frame = Frame(self.mainWindow, bg=bgColour)

        # Setting up frames within "frame" to make it easier to arrange the components using .pack()
        frameSelectionBox = Frame(frame, bg=bgColour)   # Frame of list of available images
        frameImgViewer = Frame(frame, bg=butColour)     # Frane to view the currently selected image


        # If we are in delete mode, create approporiate instructions for the user and create a delete button
        if mode == "delete":
            subtitle = Label(frame, text='Select the desired image(s) and press the "DELETE" button.\n\nTo go back, select "View" and choose the desired album.', font=("Verdana", 10), fg=txtColour, bg=bgColour)
            subtitle.pack(pady=(15,0))

            button = Button(frame, text="DELETE", font=("Verdana", 10), fg=butTxtColour, bg=butColour, command=lambda:self.Delete(listOfImages, self.imgListBoxWidget.curselection()))
            button.pack(anchor=W, padx=25, pady=(15, 3))

        # If we are in download mode, create approporiate instructions for the user and create a download button    
        elif mode == "download":
            subtitle = Label(frame, text='Select the desired image(s) and press the "DOWNLOAD" button.\nThen, select a download location.\n\nTo go back, select "View" and choose the desired album.', font=("Verdana", 10), fg=txtColour, bg=bgColour)
            subtitle.pack(pady=(15,0))

            button = Button(frame, text="DOWNLOAD", font=("Verdana", 10), fg=butTxtColour, bg=butColour, command=lambda:self.Download(listOfImages, self.imgListBoxWidget.curselection()))
            button.pack(anchor=W, padx=25, pady=(15,3))

        # If we are in view mode (which is the default), tell the user what album they are currently viewing
        else:
            if privOrPublic == AlbumView.PRIVATE:
                subtitle = Label(frame, text="Your Private Album", font=("Verdana", 15), fg=txtColour, bg=bgColour)
                subtitle.pack(pady=15)
            elif privOrPublic == AlbumView.PUBLIC:
                subtitle = Label(frame, text="The Public Album", font=("Verdana", 15), fg=txtColour, bg=bgColour)
                subtitle.pack(pady=15)


        # Setting up the scroll bars for the image selection box
        yDirScrollBar = Scrollbar(frameSelectionBox)
        yDirScrollBar.pack(side=RIGHT, fill=Y)

        xDirScrollBar = Scrollbar(frameSelectionBox, orient=HORIZONTAL)
        xDirScrollBar.pack(side=BOTTOM, fill=X)
        

        # Setting up the image selection box where all available image options are displayed
        self.imgListBoxWidget = Listbox(frameSelectionBox, selectmode=EXTENDED, yscrollcommand=yDirScrollBar.set, xscrollcommand=xDirScrollBar.set, bg=butColour, fg=butTxtColour, font = "Verdana", width=20)
        # Enable multi-select if we are in delete or download mode
        if mode == "delete" or mode == "download":
            self.imgListBoxWidget.configure(selectmode=MULTIPLE)
        else:
            self.imgListBoxWidget.configure(selectmode=SINGLE)


        # Configuring the scoll bars to control the image selection box
        yDirScrollBar.config(command=self.imgListBoxWidget.yview)
        xDirScrollBar.config(command=self.imgListBoxWidget.xview)


        # Getting a list of the images in the current album being viewed (either user's private album or the public album)
        listOfImages = None
        if self.currentAlbum == AlbumView.PRIVATE:
            listOfImages = self.databaseOfUsers.GetPhotos(AlbumView.PRIVATE, self.currentUser)
            if debug : print(self.currentUser + " Images:")
        elif self.currentAlbum == AlbumView.PUBLIC:
            listOfImages = self.databaseOfUsers.GetPhotos(AlbumView.PUBLIC)
            if debug : print("Public Images:")
        

        # For each image, add it as one of the options in the image selection box
        for image in listOfImages:
            if debug : print("  " + image)
            self.imgListBoxWidget.insert(END, image)


        # Setting up the image viewer box and configuing it
        imgViewer = Label(frameImgViewer, text="Please select a photo to view it.\n\n\nIf there is nothing listed on the left, then no photos have been uploaded yet.", font=("Verdana", 10), fg=txtColour, image=self.currentImage, bg=butColour)
        imgViewer.configure(wraplength=imgViewer.winfo_width(), justify=CENTER)
        imgViewer.bind('<Configure>', lambda e: imgViewer.config(wraplength=imgViewer.winfo_width()))
        imgViewer.pack(padx=25, pady=25, fill=BOTH, expand=True)


        # Binding the image selection box to the image handler whenever an item is selected
        # If we are in delete or edit mode, then we are using a multi-selection box (so the list box is of type "multiple")
        if mode == "delete" or mode == "download":
            self.imgListBoxWidget.bind('<<ListboxSelect>>', lambda event:self.ImageHandler(event, "multiple", listOfImages, imgViewer))
        # If we are in view mode (the default mode), then we are using a single-selection box (so the list box is of type "single")
        else:
            self.imgListBoxWidget.bind('<<ListboxSelect>>', lambda event:self.ImageHandler(event, "single", listOfImages, imgViewer))
        # Packing the image selection box
        self.imgListBoxWidget.pack(fill=BOTH, expand=True)


        # Packing the frames within "frame"
        frameSelectionBox.pack(fill=Y, side=LEFT, padx=25)
        frameImgViewer.pack(fill=BOTH, expand=True, side=LEFT, padx=25)


        # Packing the main "frame"
        frame.pack(fill=BOTH, expand=True, pady=(0,25))

        return frame


    # Confirm new user is vaild and then go back to start screen
    def CreateUser(self, username, password, passwordConfirm):
        # Convert username is all uppercase
        username = username.upper()

        # If username is alphanumeric (only letters or numbers and no specical characters), then it is okay so continue checking
        if username.isalnum() == True:
            # Check to see if the entered passwords match
            if password == passwordConfirm:
                # Try to create a new unique user
                newUniqueUser = self.databaseOfUsers.CreateUser(username, password)
                # If we can successfully create a new user, then continue and return to starting frame to let them login
                if newUniqueUser == ExitCode.SUCCESS:
                    messagebox.showinfo("Success", "Welcome, " + username + "!\nYour account was successfully created.\n\n")
                    self.SwitchFrame(self.StartFrame())
                # If we can't create a new unique user, then that username already exist in the database
                else:
                    messagebox.showerror("Attention: Username Taken", "That username is already taken!")
            # If the passwords do not match, then show error
            else:
                messagebox.showerror("Attention: Invaild Password", "The passwords do not match!\n\nNote: Passwords are case-sensitive.")
        # If the username is not alphanumeric, show error
        else:
            messagebox.showerror("Attention: Invaild Username", "This username is not allowed!\n\nNote: Usernames can only contain letters and numbers. Spaces and special charaters (such as !, $, #, @) are NOT allowed.")


    # Handles the image viewer to ensure it displays the currently selected image
    def ImageHandler(self, event, selectionType, listOfImages, imgViewerWidget):

        # Stores the index of the currently selected image in "listOfImages"
        indexOfSelection = None


        # If list box selection type is "single", then get the currently selected image normally
        if selectionType == "single":
            indexOfSelection = int(self.imgListBoxWidget.curselection()[0])

        # If list box selection type is "multiple", then find the most recently selected image by comparing all the 
        # current selections in "listOfSelections" to the previous list of selection images (self.listOfPriorSelections)
        # to spot the difference
        elif selectionType == "multiple":
            listOfSelections = self.imgListBoxWidget.curselection()

            # Find what image is different in the two list (which indicates it was either the last selected or it was just unselected)
            lastSelectedItem = set(listOfSelections).symmetric_difference(set(self.listOfPriorSelections))
            indexOfSelection = int(list(lastSelectedItem)[0])

            # Update list of old image selections to the current list of selections for next time
            self.listOfPriorSelections = listOfSelections


        # Get name of currently select image now that we have found the correct index
        imgName = listOfImages[indexOfSelection]

        # Open the directory where all the images are stored for the current album being viewed
        self.databaseOfUsers.OpenPhotoDir(self.currentAlbum, self.currentUser)

        # Open the image in that directory
        img = Image.open(imgName)

        #Stores tuple of image size in the format (width, height) for the currently selected image
        sizeOfImg = img.size

        # Find the largest side of the image. If "largestSideOfImg" is none, both sides are equal and its a square. If it
        # is zero, the largest side is the width. If it is one, the largest side is the height
        largestSideOfImg = None
        if sizeOfImg[0] != sizeOfImg[1]:
            largestSideOfImg = sizeOfImg.index(max(sizeOfImg))
        
        # Calculate the image ratio of the width to the height
        ratio = sizeOfImg[0]/sizeOfImg[1]

        # Stores the size of the image viewer widget in the form [width, height]
        sizeOfImgViewer = [imgViewerWidget.winfo_width(), imgViewerWidget.winfo_height()]


        # *** DETERMING THE HEIGHT AND WIDTH OF THE IMAGE TO FIT WITHIN THE IMAGE VIWER ***
        #If width is largest side of image, adjust the width to fill the image viewer frame completely
        if largestSideOfImg == 0:
            imgWidth = int(imgViewerWidget.winfo_width())
            imgHeight = int(imgWidth*(1/ratio))
            #If the new height of the image is larger than the height of the frame, then it won't fit properly vertically so size it down 
            if imgHeight > sizeOfImgViewer[1]:
                #New image height is calculated by subtracting different between the current height and the image viewer height
                imgHeight = int(imgHeight - (imgHeight - sizeOfImgViewer[1]))
                imgWidth = int(imgHeight*ratio)

        #Else, if height of image is largest, adjust image height to fill the image viewer frame completely
        elif largestSideOfImg == 1:
            imgHeight = int(imgViewerWidget.winfo_height())
            imgWidth = int(imgHeight*ratio)

            #If the new width of the image is larger than the width of the frame, then it won't fit properly horizontally so size it down 
            if imgWidth > sizeOfImgViewer[0]:
                #New image width is calculated by subtracting different between the current width and the image viewer width
                imgWidth = int(imgWidth - (imgWidth - sizeOfImgViewer[0]))
                imgHeight = int(imgWidth*(1/ratio))
        
        #Else, if image is a square, then size it up to fill the smallest side of the image viewer frame
        elif largestSideOfImg == None:
            #If width of image viewer is smaller than its height, make the width of the image itself as large as the image viewer frame width
            if sizeOfImgViewer[0] < sizeOfImgViewer[1]:
                imgWidth = int(imgViewerWidget.winfo_width())
                imgHeight = int(imgWidth*(1/ratio))
            #If height of image viewer is smaller than (or equal to) its height, make the height of the image itself as large as the image viewer frame height
            else:
                imgHeight = int(imgViewerWidget.winfo_height())
                imgWidth = int(imgHeight*ratio)

        # Reszie image to fit within the image viewer frame
        img = img.resize((imgWidth, imgHeight), Image.ANTIALIAS)

        # Update the global object variable that stores a reference to the current image being displayed
        self.currentImage = ImageTk.PhotoImage(img)

        # Reconfigure the image viewer to display the current image
        imgViewerWidget.configure(image=self.currentImage)
        
        # Close the directory of photos for the current album and return to the top level application directory
        self.databaseOfUsers.ClosePhotoDir(self.currentAlbum, self.currentUser)


    # Upload images to the database
    def Upload(self):
        self.databaseOfUsers.UploadPhotos(self.currentAlbum, self.currentUser)
        self.SwitchFrame(self.HomeFrame(self.currentAlbum))


    # Delete a given list of images from the database
    def Delete(self, imgList, deletionIndices):
        self.databaseOfUsers.DeletePhotos(self.currentAlbum, imgList, deletionIndices, self.currentUser)
        self.SwitchFrame(self.HomeFrame(self.currentAlbum))


    # Download a given list of images from the database
    def Download(self, imgList, downloadIndices):
        self.databaseOfUsers.DownloadPhotos(self.currentAlbum, imgList, downloadIndices, self.currentUser)
        self.SwitchFrame(self.HomeFrame(self.currentAlbum))


    # Selects all images in the image selection list box widget
    def SelectAll(self):
        self.imgListBoxWidget.select_set(0,END)
        


# Class for the user database (stores all the users and their photos)
class UserDatabase:
    # Inital setup
    def __init__(self, databaseName):
        self.databaseName = databaseName        # Store the name of this database
        self.users = {}                         # Dictonary storing all the users in the form {key=username: value=password}

        # Constant values used for encryption
        self.uConst = 17
        self.pConst = 23

        # If path does not yet exist, create a folder within the top level application folder that will store this database
        if not os.path.exists(databaseName):
            os.mkdir(databaseName)

        # If this database does not exist yet, then we need to setup a textfile storing the users
        if not os.path.exists(databaseName + "/UserData.txt"):
            file = open(databaseName + "/UserData.txt", "x")
            file.close()

        # If this database does not exist yet, create "Users" folder to store all the data for every user
        if not os.path.exists(databaseName + '/Users'):
            os.mkdir(databaseName + '/Users')

        # If this database does not exist yet, create "Public" folder to store all the public data
        if not os.path.exists(databaseName + '/Public'):
            os.mkdir(databaseName + '/Public')


    # Encrypt usernames and passwords
    # This can be used to be store encypted account data textfiles or to encrpyt directory names (which helps keep user files somewhat 
    # since they are not stored in a folder with the same name as the user's username)
    def Encrypt(self, encryptType, dataType, data):
        # Stores each character of the encrypted name
        newData = []

        # Constant used for encryption
        const = None

        # Set the constant depending on whether the data to be encypted is a username or password
        if dataType == "username":
            const = self.uConst
        elif dataType == "password":
            const = self.pConst

        # If the data to be encrypted is for a textfile, then use this encryption method
        if encryptType == "txt":
            # For every character in the data, find the new character by adding the constant
            for char in data:
                newNum = ord(char) + const

                # If the new character goes outside of the ascii table, loop it back around from ascii 33 (so add 32) since the first 32 
                # are control characters and NOT printable characters
                if newNum > 126:
                    newNum = (newNum-126)+32
                
                # Convert new new ascii number to a character
                newChar = chr(newNum)
                # Add this new character to the list storing each new encrypted character
                newData.append(newChar)

            # Join the encrypted characters and return them as a string
            return ''.join(newData)
        
        # If the data to be encrypted is for a directory, use this method since it has to be alphanumeric
        elif encryptType == "dir":
            # All alphanumeric characters will be mapped to a new set of values called "Cypher" as seen below:
            #
            #    Char:  A   B  ... Y   Z  | 0   1  ... 8   9  | a   b  ... y   z
            #   ASCII:  65  66 ... 89  90 | 48  49 ... 56  57 | 97  98 ... 121 122
            # ----------------------------|-------------------|----------------------
            #  Cypher:  0   1  ... 24  25 | 26  27 ... 34  35 | 36  37 ... 60  61


            # For every character in the data...
            for char in data:
                num = ord(char)     # Store cypher value of original character
                cypherNum = None    # Store encrypted cypher value number that corresponds with the given character
                encodedNum = None   # Store ascii value of encrypted character

                # Convert ascii value for the character (num) into its corresponding number on the cypher
                if char >= 'A' and char <= 'Z':
                    num = ord(char) - 65
                elif char >= '0' and char <= '9':
                    num = ord(char) - 48 + 26
                elif char >= 'a' and char <= 'z':
                    num = ord(char) - 97 + 36


                # Now, since the cypher is all properly space unlike the ascii values of the alphanumeric characters, add the constant
                cypherNum = num + const

                # If adding constants exceeds the length of the cypher, wrap it around back to the start
                if cypherNum > 61:
                    #62 items in cypher, so it has to be 61+1 since cypher starts at 0.
                    cypherNum -= (61+1)

                # Convert from the encrypted cypher value back into ascii
                if cypherNum >= 0 and cypherNum <= 25:
                    encodedNum = cypherNum + 65
                elif cypherNum >= 26 and cypherNum <= 35:
                    encodedNum = cypherNum + (48 - 26)
                elif cypherNum >= 36 and cypherNum <= 61:
                    encodedNum = cypherNum + (97 - 36)
                
                # Save the charater corresponding with the ascii value
                newChar = chr(encodedNum)
                # Append this character to the list of encrypted characters
                newData.append(newChar)

            # Join the encrypted characters and return them as a string
            return ''.join(newData)


    # Decrypt usernames and passwords
    def Decrypt(self, decryptType, dataType, data):
        # NOTE: This is basically the reverse of the "Encrypt" method above

        newData = []

        const = None

        if dataType == "username":
            const = self.uConst
        elif dataType == "password":
            const = self.pConst

        if decryptType == "txt":
            for char in data:
                newNum = ord(char) - const
                if newNum < 33:
                    newNum = (newNum+126)-32
                newChar = chr(newNum)
                newData.append(newChar)
            return ''.join(newData)
        
        elif decryptType == "dir":
            #    Char:  A   B  ... Y   Z  | 0   1  ... 8   9  | a   b  ... y   z
            #   ASCII:  65  66 ... 89  90 | 48  49 ... 56  57 | 97  98 ... 121 122
            # ----------------------------|-------------------|----------------------
            #  Cypher:  0   1  ... 24  25 | 26  27 ... 34  35 | 36  37 ... 60  61

            for char in data:
                num = None
                cypherNum = None
                decodedNum = None

                if char >= 'A' and char <= 'Z':
                    num = ord(char) - 65
                elif char >= '0' and char <= '9':
                    num = ord(char) - 48 + 26
                elif char >= 'a' and char <= 'z':
                    num = ord(char) - 97 + (26+10)

                cypherNum = num - const
                if cypherNum < 0:
                    #62 items in cypher, so it has to be 61+1 since cypher starts at 0.
                    cypherNum += (61+1)

                if cypherNum >= 0 and cypherNum <= 25:
                    decodedNum = cypherNum + 65
                elif cypherNum >= 26 and cypherNum <= 35:
                    decodedNum = cypherNum + (48 - 26)
                elif cypherNum >= 36 and cypherNum <= 61:
                    decodedNum = cypherNum + (97 - 36)
                
                newChar = chr(decodedNum)

                newData.append(newChar)

            return ''.join(newData)


    # Reading existing users in the database from the textfile
    def ReadExistingUsers(self):
        # Open file
        file = open(self.databaseName + "/UserData.txt", "r")

        # Read all lines and store them in a list
        lines = file.readlines()

        if debug : print('Existing User Info (in the form "username: password"):')

        # Read each line and add the decrypted usernames and passwords to the dictonary of users
        for i in range(0, len(lines), 2):
            encryptedUsername = lines[i].rstrip('\n')
            encryptedPassword = lines[i+1].rstrip('\n')

            username = self.Decrypt("txt", "username", encryptedUsername)
            password = self.Decrypt("txt", "password", encryptedPassword)

            self.users[username] = password

            if debug : print("  " + username + ": " + password)

        # Close file
        file.close()


    # Create a new user and check to see if the username is unique
    def CreateUser(self, username, password):
        # If username does not yet exist, create the user
        if username not in self.users:
            # Add them to the dictonary of users
            self.users[username] = password

            # Make an encrypted directory name to store their folders
            os.mkdir(self.databaseName + '/Users/' + self.Encrypt("dir", "username", username))

            # Open the textfile storing account data and record their encrypted username and password
            file = open(self.databaseName + "/UserData.txt", "a")
            file.write(self.Encrypt("txt", "username", username) + "\n")
            file.write(self.Encrypt("txt", "password", password) + "\n")
            file.close()

            return ExitCode.SUCCESS

        return ExitCode.ERROR


    # Validate user to see if the correct username and password was entered
    def ValidateUser(self, username, password):
        # Username is dictonary key. Password is dictonary value
        for key, value in self.users.items():
            if key == username:
                if value == password:
                    return ExitCode.SUCCESS
        return ExitCode.ERROR


    # Open directory of the requested album type (private or public). If opening private album, specify the username of the 
    # user files you want to access
    def OpenPhotoDir(self, privOrPublic : AlbumView, username=None):
        os.chdir(topLevelDir)

        if privOrPublic == AlbumView.PUBLIC:
            os.chdir(self.databaseName)
            os.chdir('Public')

        elif privOrPublic == AlbumView.PRIVATE and username != None:
            os.chdir(self.databaseName)
            os.chdir('Users')
            os.chdir(self.Encrypt("dir", "username", username))

        else:
            return ExitCode.ERROR

        return ExitCode.SUCCESS


    # Close directory of the requested album type (private or public). If closing a private album, specify the username
    def ClosePhotoDir(self, privOrPublic : AlbumView, username=None):
        # If public album folder is open, return to top-level application directory
        if privOrPublic == AlbumView.PUBLIC:
            if 'Public' == os.path.basename(os.getcwd()):
                os.chdir(topLevelDir)

        # If private album folder is open, check to see if the enter username matches the current directory and then return
        # to the top-level application directory
        elif privOrPublic == AlbumView.PRIVATE and username != None:
            if self.Decrypt("dir", "username", username) == os.path.basename(os.getcwd()):
                os.chdir(topLevelDir)

        else:
            return ExitCode.ERROR

        return ExitCode.SUCCESS


    # Get a list of images in a given album (private or public). If getting photos from a private album, specify the username.
    def GetPhotos(self, privOrPublic : AlbumView, username=None):
        # If public album, get all the files that end with image extensions and return them as a list
        if privOrPublic == AlbumView.PUBLIC:
            self.OpenPhotoDir(AlbumView.PUBLIC)

            listOfImgFiles = []

            for file in os.listdir(os.getcwd()):
                tmpName = file.lower()
                if tmpName.endswith(".jpg") or tmpName.endswith(".jpeg") or tmpName.endswith(".png") or tmpName.endswith(".gif"):
                    listOfImgFiles.append(file)

            self.ClosePhotoDir(AlbumView.PUBLIC)

            return listOfImgFiles

        # If private album, open the user's folder and get all the files that end with image extenstions. Then, return them as a list
        elif privOrPublic == AlbumView.PRIVATE and username != None:
            self.OpenPhotoDir(AlbumView.PRIVATE, username)

            listOfImgFiles = []

            for file in os.listdir(os.getcwd()):
                tmpName = file.lower()
                if tmpName.endswith(".jpg") or tmpName.endswith(".jpeg") or tmpName.endswith(".png") or tmpName.endswith(".gif"):
                    listOfImgFiles.append(file)

            self.ClosePhotoDir(AlbumView.PRIVATE, username)

            return listOfImgFiles


        else:
            return ExitCode.ERROR


    # Upload photos to a given album. If uploading to a private album, specify the username
    def UploadPhotos(self, privOrPublic : AlbumView, username=None):   
        # Depdning on album type, open file selection window with custom title telling the user what to do
        if privOrPublic == AlbumView.PUBLIC:
            fileDirectories = filedialog.askopenfilenames(initialdir="/", title = "Select image(s) to publicly upload...",filetypes = (("JPG files","*.jpg"),("JPEG files","*.jpeg"),("PNG files","*.png"), ("GIF files","*.gif")))
            self.OpenPhotoDir(AlbumView.PUBLIC)
        elif privOrPublic == AlbumView.PRIVATE:
            fileDirectories = filedialog.askopenfilenames(initialdir="/", title = "Select image(s) to privately upload...",filetypes = (("JPG files","*.jpg"),("JPEG files","*.jpeg"),("PNG files","*.png"), ("GIF files","*.gif")))
            self.OpenPhotoDir(AlbumView.PRIVATE, username)

        # For all the selected files, copy them into the database
        for fileDir in fileDirectories:  
            imgName = os.path.basename(fileDir)
            # If file name already exist, asl user if they would like to override the current file in the database
            if os.path.exists(imgName):
                answer = messagebox.askquestion("Attention: File already exist", "The file " + imgName + " already exist in this album.\n\nWould you like to override the existing image in the repository?")
                if answer == 'yes':
                    shutil.copy(fileDir, os.getcwd())
                    if debug : print(imgName + " was uploaded!")
            else:
                shutil.copy(fileDir, os.getcwd())


        # Close the directory
        if privOrPublic == AlbumView.PUBLIC:
            self.ClosePhotoDir(AlbumView.PUBLIC)
        elif privOrPublic == AlbumView.PRIVATE:
            self.ClosePhotoDir(AlbumView.PRIVATE, username)


    # Delete photos from a given album. If deleting from a private album, specify the username
    def DeletePhotos(self, privOrPublic : AlbumView, imageList, deletionIndices, username=None):
        # Open proper directory
        if privOrPublic == AlbumView.PUBLIC:
            self.OpenPhotoDir(AlbumView.PUBLIC)
        elif privOrPublic == AlbumView.PRIVATE:
            self.OpenPhotoDir(AlbumView.PRIVATE, username)

        # For every index in the list of indicies, get the corresponding image name in the imageList
        for index in deletionIndices:
            imgName = imageList[index]
            # Try to remove image from the database directory
            try:
                os.remove(imgName)
                if debug : print (imgName + " was deleted!")
            # If unsuccessful, tell user unable to delete file
            except:
                messagebox.showerror("Attention: Unable to Delete File", "There was an error when try to delete " + imgName + " from the repository.")


        # Close directory
        if privOrPublic == AlbumView.PUBLIC:
            self.ClosePhotoDir(AlbumView.PUBLIC)
        elif privOrPublic == AlbumView.PRIVATE:
            self.ClosePhotoDir(AlbumView.PRIVATE, username)


    # Download photos from a given album. If downlading from a private album, specify the username
    def DownloadPhotos(self, privOrPublic : AlbumView, imageList, downloadIndices, username=None):
        # Get user to set the target download directory in a folder selection window
        targetDirectory = filedialog.askdirectory(initialdir="/", title = "Select download location...")

        # Open proper directory
        if privOrPublic == AlbumView.PUBLIC:
            self.OpenPhotoDir(AlbumView.PUBLIC)
        elif privOrPublic == AlbumView.PRIVATE:
            self.OpenPhotoDir(AlbumView.PRIVATE, username)

        # For every index in the list of indices, download the corresponding item in imgList
        for index in downloadIndices:  
            imgName = imageList[index]
            # If file with same name already exist at the target download location, ask user if they would like to override it
            if os.path.exists(targetDirectory + "/" + imgName):
                answer = messagebox.askquestion("Attention: File already exist", "The file " + imgName + " already exist in this folder.\n\nWould you like to override your existing image with the repository download?")
                if answer == 'yes':
                    shutil.copy(imgName, targetDirectory)
                    if debug : print(imgName + " was downloaded to " + targetDirectory)
            else:
                shutil.copy(imgName, targetDirectory)

        # Close directory
        if privOrPublic == AlbumView.PUBLIC:
            self.ClosePhotoDir(AlbumView.PUBLIC)
        elif privOrPublic == AlbumView.PRIVATE:
            self.ClosePhotoDir(AlbumView.PRIVATE, username)

        messagebox.showinfo("Success", "The download has been completed! You can find your downloaded images here:\n\n" + targetDirectory)





# Setup user database object with the name "Database"
database = UserDatabase("Database")

# Read all the existing users in this database
database.ReadExistingUsers()


# Setup application object where the GUI will run from
application = ImgRepGUI(database)

# Run application
application.Run()

