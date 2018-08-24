from tkinter import * #import resources for GUI
from tkinter import ttk
from tkinter.filedialog import askdirectory
import os
import shutil


## DEFINE FUNCTIONS AND VARIABLES
dirPath=""

def openDirectory():
  global dirPath
  dirPath = askdirectory(parent=root, initialdir="/", mustexist=True, title = "Choose a directory to organize")
  pathLabel.config(text=dirPath)
  
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
    print("move complete")
  else:
    print ("path does not exist")

def client_exit():
  exit()



## INITIALIZE SETTINGS
root = Tk() #create window root
root.geometry("800x600") #set size of window
Title = root.title("File Opener") #set title of window



## CREATE MENU BAR
menu = Menu(root)
root.config(menu=menu)

file = Menu(menu)
file.add_command(label = 'Open')
file.add_command(label = 'Exit', command = client_exit)

menu.add_cascade(label = 'File', menu = file)



## CREATE MAIN CONTENT
browseButton = Button(root, text="Browse", command=openDirectory)
browseButton.pack()

pathLabel = Label(root)
pathLabel.pack()

organizeButton = Button(root, text="Organize", command= organizeFiles)
organizeButton.pack()



root.mainloop() #show window and begin main loop