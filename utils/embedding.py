from pydub import AudioSegment as audio
from random import randrange, sample, shuffle
from math import ceil
from functools import reduce

class Embedding:
    def __init__(self, positives, negatives, backgrounds, destination):
        self.positives = positives
        self.negatives = negatives
        self.backgrounds = backgrounds
        self.destination = destination

        self.negatives_range = (1,4)
        self.positives_range = (1,3)
        self.margin_range = (100, 1000)
        
        self.background_dBFS = -50

    def randomChunks(self, array, chunk_range):
        array_copy = array.copy()
        result = []
        while array_copy:
            size = min(len(array_copy),randrange(*chunk_range))
            subarray = [array_copy.pop(randrange(len(array_copy))) for _ in range(size)]
            result.append(subarray)
        return result

    def loadTracks(self, tracks, label=0):
        loaded = []
        for path in tracks:
            _, ext = path.split('.')
            track = audio.from_file(path, ext)
            loaded.append((track, label))
        return loaded

    
    def loadRandomBackground(self, size):
        backgrounds_amount = len(self.backgrounds)
        silent_probability = 0.15
        zeros_amount = ceil(backgrounds_amount*silent_probability)
        zeros = [0 for _ in range(zeros_amount)]
        path, = sample([*zeros, *self.backgrounds], 1)
        if path:
            _, ext = path.split('.')
            begin = randrange(0, size)
            
            background = audio.from_file(path, ext)
        
            dBFS_change = background.dBFS - self.background_dBFS
            background = background.apply_gain(dBFS_change)
            background = background[begin:begin+size]
        else:
            background = audio.silent(duration=size)
        
        return background

    def joinTracksWithRandomMargins(self, margin_range):
        def reducer(connected, loaded):
            recording, timestamps = connected
            track, label = loaded

            margin = randrange(*margin_range)
            silence = audio.silent(duration=margin)

            if label:
                begin = len(recording)+len(silence)
                end = begin+len(track)
                timestamps.append((begin, end))
            
            recording = recording + silence + track
            return (recording, timestamps)
        return reducer

    def connectTracks(self, *loaded):
        loaded_list = [el for sublist in loaded for el in sublist]
        shuffle(loaded_list)

        initial = [audio.empty(), []]
        connected = reduce(
            self.joinTracksWithRandomMargins(self.margin_range),
            loaded_list,
            initial
        )
        return connected

    def putOnBackground(self, background, recording):
        end_margin = randrange(*self.margin_range)
        recording = recording + audio.silent(duration=end_margin)

        result_audio = background.overlay(recording)
        return result_audio

    def saveAllToWav(self, recordings):
        for i, recording in enumerate(recordings):
            new_filename = f'{self.destination}/track-{i}.wav'
            recording = recording.set_frame_rate(44100)
            recording = recording.set_sample_width(2)
            recording.export(new_filename, format='wav')

