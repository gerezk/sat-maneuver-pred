import argparse
import os

from preprocess import Preprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scc', type=str, default='', help='Five-digit NORAD ID')
    args = parser.parse_args()

    # Preprocess TLEs
    if not os.path.exists('./data/preprocessed'):
        os.makedirs('./data/preprocessed')
    if not os.path.exists(f'./data/preprocessed/{args.scc}.csv'):
        Preprocess(args)