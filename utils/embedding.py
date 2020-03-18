from pydub import AudioSegment as audio
from random import randrange, sample
from functools import reduce

class Embedding:
    def __init__(self, positives, negatives, backgrounds):
        self.positives = positives
        self.negatives = negatives
        self.backgrounds = backgrounds

        self.negatives_range = (0,4)
        self.positives_range = (0,3)
        self.margin_range = (100, 1000)
        
        self.background_dBFS = -50

    
    
    def loadRandomBackground(self, size):
        path, = sample(self.backgrounds, 1)
        _, ext = path.split('.')
        begin = randrange(0, size)
        
        background = audio.from_file(path, ext)
        background = background[begin:begin+size]
        
        dBFS_change = background.dBSF - self.background_dBFS
        background = background.apply_gain(dBFS_change)

        return background