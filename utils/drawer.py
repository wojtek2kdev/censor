import numpy as np
import pydub as pdb
import librosa
import argparse, sys, os

from tqdm import tqdm
from pathlib import Path
from math import ceil, floor

class Drawer:
    def __init__(self, tracks_info, destination=os.getcwd(), out='data.npy'):
        self.hop_length = 512
        self.result = None
        
        self.tracks_info = tracks_info
        self.destination = f'{destination}/{out}'

    def generateSpectrogram(self, time_series, sample_rate):
        spectrogram = librosa.feature.melspectrogram(y=time_series, sr=sample_rate, hop_length=self.hop_length)
        reshaped_spectrogram = spectrogram.T #Want to timesteps first
        return reshaped_spectrogram

    def timestampScale(self, timestamp, time_series, sample_rate, mel_timesteps_amount):
        duration_ms = floor(librosa.get_duration(y=time_series, sr=sample_rate)*1000)
        begin, end = timestamp
        scaled_begin = floor((begin/duration_ms)*mel_timesteps_amount)
        scaled_end = min(mel_timesteps_amount, ceil((end/duration_ms)*mel_timesteps_amount))
        return (scaled_begin, scaled_end)

    def generateDesiredOutput(self, mel_timesteps_amount, timestamps):
        output = np.zeros(mel_timesteps_amount)
        for timestamp in timestamps:
            begin, end = timestamp
            output[begin:end] = 1
        return output
            
    def save(self):
        print('Saving..')
        np.save(self.destination, self.result)
    
    def process(self):
        data = []
        progress = tqdm(total=len(self.tracks_info), desc='Spectrograms generating')
        for path, timestamps in self.tracks_info:
            time_series, sample_rate = librosa.load(path)

            melspectrogram = self.generateSpectrogram(time_series, sample_rate)
            mel_timesteps_amount, _ = melspectrogram.shape
            scaled_timestamps = [self.timestampScale(timestamp, time_series, sample_rate, mel_timesteps_amount) for timestamp in timestamps]
            
            desired_output = self.generateDesiredOutput(mel_timesteps_amount, scaled_timestamps)

            data.append([melspectrogram, desired_output])
            progress.update(1)
        self.result = np.array(data).T
