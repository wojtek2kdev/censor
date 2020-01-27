from tkinter import *
from tkinter import filedialog

import pandas as pd

from youtube_dl import YoutubeDL

class Downloader:

    def __init__(self, **kwargs):
        self._start_from_checkpoint = kwargs.get('checkpoint', True)
        self._extension = kwargs.get('extension', 'm4a')

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
        csv = pd.read_csv(filename, sep=';')
        if self._start_from_checkpoint:
            csv = csv[csv['id'] > csv[csv['checkpoint']==1]['id'][1]]
        sources = []
        for index, row in csv.iterrows():
            data = {
                'id': int(row.id), 
                'link': row.link, 
                'start': row.start, 
                'stop': row.stop
            }
            sources.append(data)
        return sources

    def downloadTracks(self):
        sources = self.loadSources()
        directory = self.getDirectory()

        downloaded = 0

        for source in sources:       
            ydl_opts = {
                'format': 'bestaudio[ext={}]'.format(self._extension),
                'outtmpl': directory + '/%(id)s.%(ext)s',
                'prefer_ffmpeg': True,
                'quiet': True,
                'postprocessor_args': [
                    '-ss', 
                    source['start'],
                    '-to',
                    source['stop']
                ]
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([source['link']])
                downloaded += 1
                print("[{}/{}] Tracks downloaded".format(downloaded, len(sources))) 

d = Downloader(checkpoint=False)
d.downloadTracks()