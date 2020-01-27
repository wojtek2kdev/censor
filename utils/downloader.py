from tkinter import *
from tkinter import filedialog

def getFilename():
    Tk().withdraw()
    filename = filedialog.askopenfilename(
        initialdir='.',
        title='Select file with sources'
    )
    return filename

