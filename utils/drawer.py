import numpy as np
import pydub as pdb
import librosa
import argparse, sys, os

from tqdm import tqdm
from pathlib import Path

def main(args):
    source_dir = Path(args.dir).resolve()
    destination = Path(args.dest).resolve()
    clear_destination = args.clear
    
    def clear_dir(directory):
        for root, dirs, files in os.walk(directory):
                for file in files:
                    os.remove(os.path.join(root, file))

    def convert_to_wav(filename):
        name, ext = filename.split('.')
        audio = pdb.AudioSegment.from_file(f'{source_dir}/{filename}', ext)
        audio = audio.set_frame_rate(44100)
        audio = audio.set_sample_width(2)
        new_path = f'{destination}/{name}.wav'
        audio.export(new_path, format='wav')
        return new_path

    def generate_spectrogram(filename):
        path, _ = filename.split('.')
        time_series, sample_rate = librosa.load(filename)
        spectrogram = librosa.feature.melspectrogram(y=time_series, sr=sample_rate)
        reshaped_spectrogram = spectrogram.T #Want to timesteps first
        np.save(f'{path}.npy', reshaped_spectrogram)

    if clear_destination:
        clear_dir(destination)

    tracks = os.listdir(source_dir)
    progress = tqdm(total=len(tracks), desc='Spectrograms generating')
    for i, track in enumerate(tracks):
        new_path = convert_to_wav(track)
        generate_spectrogram(new_path)
        progress.update(1)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='Specify audio files localization.')
    parser.add_argument('--dest', help='Specify spectrograms destination dir.')
    parser.add_argument('--clear', action='store_true', help="Clear destination dir.")
    args = parser.parse_args()
    main(args)