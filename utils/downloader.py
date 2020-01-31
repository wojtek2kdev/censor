from tkinter import *
from tkinter import filedialog
from youtube_dl import YoutubeDL
from threading import Thread
from tqdm import *
from time import time

import pandas as pd
import numpy as np

class Downloader:

    def __init__(self, **kwargs):
        self._ignore_downloaded = kwargs.get('ignore_downloaded', True)
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

    def convertTimestamp(self, timestamp):
        seconds, miliseconds = str(timestamp).split('/')
        seconds = int(seconds)
        hour = seconds//3600
        minute = (seconds-3600*hour)//60
        second = seconds-3600*hour-60*minute
        newTimestamp = [*map(lambda t: str(t).zfill(2), [hour, minute, second, miliseconds])]
        return "{}:{}:{}.{}".format(*newTimestamp) 


    def loadSources(self):
        filename = self.getFilename()
        csv = pd.read_csv(filename, sep=';')
        if self._ignore_downloaded:
            csv = csv[csv['downloaded'] != 1]
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

    def downloadTracks(self, sources_part, directory, progress):
        for source in sources_part:     
            ydl_opts = {
                'format': 'bestaudio[ext={}]'.format(self._extension),
                'outtmpl': directory + '/{}-%(id)s-{}.%(ext)s'.format(source['id'], round(time()*1000)),
                'prefer_ffmpeg': True,
                'quiet': True,
                'postprocessor_args': [
                    '-ss', 
                    self.convertTimestamp(source['start']),
                    '-to',
                    self.convertTimestamp(source['stop'])
                ]
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([source['link']])
                progress.update(1)

    def run(self, thread_count=5):
        sources = self.loadSources()
        directory = self.getDirectory()

        bar = tqdm(total=len(sources), desc="Download")

        sources = filter(
            lambda source_list: source_list.any(),
            np.array_split(sources, thread_count)
        )

        thread_number = 1
        for sources_part in sources:
            thread = Thread(
                target=self.downloadTracks, 
                args=(sources_part, directory, bar)
            )
            thread_number += 1
            thread.start()

d = Downloader(ignore_downloaded=True)
d.run()