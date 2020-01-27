from tkinter import *
from tkinter import filedialog

def getFilename():
    Tk().withdraw()
    filename = filedialog.askopenfilename(
        initialdir='.',
        title='Select file with sources'
    )
    return filename

def getDirectory():
    Tk().withdraw()
    directory = filedialog.askdirectory(
        initialdir='.',
        title='Select destination directory for downloaded data'
    )
    return directory
    