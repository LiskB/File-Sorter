from tkinter import * #import resources for GUI
from tkinter.filedialog import askdirectory
import os
import shutil


## DEFINE FUNCTIONS AND VARIABLES
dirPath="" # Stores the path the user chooses

## This method opens the prompt dialog box for the user to choose a directory
def openDirectory():
  global dirPath
  dirPath = askdirectory(parent=root, initialdir="/", mustexist=True, title = "Choose a directory to organize")
  pathLabel.config(text=dirPath)
  
## This method brings all files to the parent directory, deletes the empty folders
## Also has the option to group files into new folders, based on user selection
def organizeFiles():
  global dirPath
  
  if os.path.exists(dirPath):
    fileList = []
    for root, _, filenames in os.walk(dirPath):
      for filename in filenames:
        if filename[0] != ".": #exclude hidden system files
          fileList.append(os.path.join(root, filename))
    
    # Add all files to parent directory
    for filepath in fileList:
      shutil.move(filepath, os.path.join(dirPath, os.path.basename(filepath)))
    # Delete the empty folders
    childrenPaths = os.listdir(dirPath)
    for childPath in childrenPaths:
      if os.path.isdir(os.path.join(dirPath, childPath)):
        shutil.rmtree(os.path.join(dirPath, childPath))
    
    # Check for organization method
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
  
  else:
    pathLabel.config(text="Error: Path not found")

## This method exits the program
def client_exit():
  exit()



## INITIALIZE SETTINGS
root = Tk() #create window root
root.geometry("550x220") #set size of window
Title = root.title("File Opener") #set title of window



## CREATE CONTENT FRAME AND MENU BAR
content = Frame(root)
'''
menubar = Menu(root)
menubar.add_command(label = "Open", command= client_exit)
menubar.add_command(label = "Exit", command = client_exit)
root.config(menu=menubar)
'''


## CREATE MAIN CONTENT
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

## LAYOUT
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



root.mainloop() #show window and begin main loop