from tkinter import *
from tkinter import filedialog

import pandas as pd

class Downloader:
    def getFilename(self):
        Tk().withdraw()
        filename = filedialog.askopenfilename(
            initialdir='.',
            title='Select file with sources'
        )
        return filename

    def getDirectory(self):
        Tk().withdraw()
        directory = filedialog.askdirectory(
            initialdir='.',
            title='Select destination directory for downloaded data'
        )
        return directory

    def loadSources(self):
        filename = self.getFilename()
        sources = pd.read_csv(filename, sep=';').to_dict()
        return sources

