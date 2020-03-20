from pathlib import Path
from embedding import Embedding
from drawer import Drawer

import argparse, os

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='positives', help='Specify positives directory path.')
    parser.add_argument('-n', dest='negatives', help='Specify negatives directory path.')
    parser.add_argument('-b', dest='backgrounds', help='Specify backgrounds directory path.')
    parser.add_argument('-d', dest='destination', help='Specify destination pirectory path.')
    parser.add_argument('-i', dest='iterations', help='Specify iterations number.')
    parser.add_argument('--out', help='Specify out filename.')
    parser.add_argument('--clear', action='store_true', help='Specify if clear destination directory.')

    args = parser.parse_args()

    positives = str(Path(args.positives).resolve())
    negatives = str(Path(args.negatives).resolve())
    backgrounds = str(Path(args.backgrounds).resolve())
    destination = str(Path(args.destination).resolve())

    iterations = int(args.iterations)

    out_filename = args.out

    positives = list(absoluteFilePaths(positives))
    negatives = list(absoluteFilePaths(negatives))
    backgrounds = list(absoluteFilePaths(backgrounds))

    if args.clear:
        for root, dirs, files in os.walk(destination):
            for file in files:
                os.remove(os.path.join(root, file))
    
    embedding = Embedding(positives, negatives, backgrounds, destination, iterations)
    tracks_info = embedding.process()

    drawer = Drawer(tracks_info, destination, out_filename)
    drawer.process()
    drawer.save()