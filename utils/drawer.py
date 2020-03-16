import numpy as np
import pydub as pdb
import librosa
import argparse, sys, os

def clear_dir(directory):
    for root, dirs, files in os.walk(directory):
            for file in files:
                os.remove(os.path.join(root, file))

def convert_to_wav(track):
    pass

def main(args):
    source_dir = args.dir
    destination = args.dest
    clear_destination = args.clear
    
    if clear_destination:
        clear_dir(destination)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='Specify audio files localization.')
    parser.add_argument('--dest', help='Specify spectrograms destination dir.')
    parser.add_argument('--clear', action='store_true', help="Clear destination dir.")
    args = parser.parse_args()
    main(args)