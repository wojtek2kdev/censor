from pydub import AudioSegment as audio
from random import randrange, sample, shuffle
from math import ceil
from functools import reduce
from itertools import repeat, zip_longest

class Embedding:
    def __init__(self, positives, negatives, backgrounds, destination):
        self.positives = positives
        self.negatives = negatives
        self.backgrounds = backgrounds
        self.destination = destination

        self.negatives_range = (1,4)
        self.positives_range = (1,3)
        self.margin_range = (100, 1000)

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
        zeros = list(repeat(0, zeros_amount))
        path, = sample([*zeros, *self.backgrounds], 1)
        if path:
            _, ext = path.split('.')
            begin = randrange(0, size)
            background = audio.from_file(path, ext)
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

    def connectTracks(self, chunk):
        shuffle(chunk)

        initial = [audio.empty(), []]
        connected = reduce(
            self.joinTracksWithRandomMargins(self.margin_range),
            chunk,
            initial
        )
        return connected

    def putOnBackground(self, background, recording):
        end_margin = randrange(*self.margin_range)
        recording = recording + audio.silent(duration=end_margin)

        result_audio = background.overlay(recording)
        return result_audio

    def saveToWav(self, recording, filename):
        new_path = f'{self.destination}/{filename}.wav'
        recording = recording.set_frame_rate(44100)
        recording = recording.set_sample_width(2)
        recording.export(new_path, format='wav')
        return new_path

    def process(self):
        positive_tracks = self.loadTracks(self.positives, 1)
        negative_tracks = self.loadTracks(self.negatives, 0)

        positive_chunks = self.randomChunks(positive_tracks, self.positives_range)
        negative_chunks = self.randomChunks(negative_tracks, self.negatives_range)

        merged_chunks = [[*n, *p] for n, p in zip_longest(positive_chunks, negative_chunks, fillvalue=[])]

        processed = []

        for i, chunk in enumerate(merged_chunks):
            track, timestamps = self.connectTracks(chunk)
            background = self.loadRandomBackground(len(track))
            
            track_on_background = self.putOnBackground(background, track)
            new_path = self.saveToWav(track_on_background, f'track-{i}')
            
            processed.append((new_path, timestamps))

        return processed
