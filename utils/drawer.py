import numpy as np
import pydub as pdb
import librosa
import argparse, sys, os


def main(args):
    source_dir = args.dir
    destination = args.dest
    clear_destination = args.clear
    
    if clear_destination:
        for root, dirs, files in os.walk(destination):
            for file in files:
                os.remove(os.path.join(root, file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='Specify audio files localization.')
    parser.add_argument('--dest', help='Specify spectrograms destination dir.')
    parser.add_argument('--clear', action='store_true', help="Clear destination dir.")
    args = parser.parse_args()
    main(args)