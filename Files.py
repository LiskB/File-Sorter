#import resources for GUI and file system
from tkinter import *
from tkinter.filedialog import askdirectory
import os
import shutil


## DEFINE FUNCTIONS AND VARIABLES
dirPath="" # Stores the path the user chooses

## This method opens the prompt dialog box for the user to choose a directory
def openDirectory():
  global dirPath
  dirPath = askdirectory(parent=root, initialdir="/", mustexist=True, title = "Choose a directory to organize")
  pathLabel.config(text=dirPath) # display the directory path
  #displayLabel.config(text="") # clear the status box
  
## This method brings all files to the parent directory, deletes the empty folders
## Also has the option to group files into new folders, based on user selection
def organizeFiles():
  global dirPath
  
  # compile list of the path of all files in the chosen directory
  if os.path.exists(dirPath):
    fileList = []
    for root, _, filenames in os.walk(dirPath):
      for filename in filenames:
        if filename[0] != ".": # exclude hidden system files
          fileList.append(os.path.join(root, filename))
    
    # Add all files to parent directory
    for filepath in fileList:
      shutil.move(filepath, os.path.join(dirPath, os.path.basename(filepath)))
    
    # Delete the empty folders
    childrenPaths = os.listdir(dirPath)
    for childPath in childrenPaths:
      if os.path.isdir(os.path.join(dirPath, childPath)):
        shutil.rmtree(os.path.join(dirPath, childPath))
    
    # Check if organization method was selected
    # if so, organize files into folders by their extension
    global typeVar
    if typeVar.get() == 1:
      fileList = os.listdir(dirPath)
      for item in fileList:
        name, extension = os.path.splitext(os.path.join(dirPath, item))
        extensionName = extension[1:].upper() # remove period from beginning of name, put in uppercase
        newPath = os.path.join(dirPath, extensionName) # define new path for file
        if not os.path.isdir(newPath):
          # if directory doesn't exist, create it
          os.makedirs(newPath)
        # add file to folder
        shutil.move(os.path.join(dirPath, item), os.path.join(newPath, item))
    displayLabel.config(text="Files organized") # update the user on the status
  
  # If the directory doesn't exist, or one wasn't entered, display this message
  else:
    pathLabel.config(text="Error: Path not found")

## This method exits the program
def client_exit():
  exit()



## INITIALIZE SETTINGS
root = Tk() # create window root
root.geometry("550x220") # set size of window
Title = root.title("File Sorter") # set title of window

content = Frame(root) # create content frame


## CREATE MAIN CONTENT
# define and pack all elements
browseButton = Button(content, text="Browse", font=("", 20), height=2, width=10, command=openDirectory)
browseButton.pack()

pathLabel = Label(content)
pathLabel.pack()

organizeLabel = Label(content, text="Organization method: ")
organizeLabel.pack()

typeVar = IntVar()
typeCheck = Checkbutton(content, text="Sort by file type", variable=typeVar)
typeCheck.pack()

organizeButton = Button(content, text="Organize", font=("", 20), height=2, width=10, command= organizeFiles)
organizeButton.pack()

displayLabel = Label(content)
displayLabel.pack()


## LAYOUT
# define a grid layout in a grid layout, so items are centered in the frame
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(2, weight=1)
content.grid(row=1, column=1)

browseButton.grid(row=0, columnspan=2)
pathLabel.grid(row=1, columnspan=2)
organizeLabel.grid(row=2)
typeCheck.grid(row=2, column=1)
organizeButton.grid(row=3, columnspan=2)
displayLabel.grid(row=4, columnspan=2)


root.mainloop() #show window and begin main loop