from pydub import AudioSegment as audio
from random import randrange, sample

class Embedding:
    def __init__(self, positives, negatives, backgrounds):
        self.positives = positives
        self.negatives = negatives
        self.backgrounds = backgrounds

        self.negatives_range = (0,4)
        self.positives_range = (0,3)
        self.margin_range = (500, 1500)
        
        self.background_dBFS = -50

    
    
    def loadRandomBackground(self, size):
        pass