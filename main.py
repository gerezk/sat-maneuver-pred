import argparse
from pathlib import Path

from preprocess import json_to_csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scc', type=str, default='', help='Five-digit NORAD ID')
    args = parser.parse_args()

    # Preprocess ELSET
    if not Path('./data/preprocessed').exists():
        Path('./data/preprocessed').mkdir()
    if not Path(f'./data/preprocessed/{args.scc}.csv').exists():
        json_to_csv(args.scc)
    # json_to_csv(args.scc)