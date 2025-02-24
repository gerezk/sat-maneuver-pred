import argparse
from pathlib import Path

from preprocess import preprocess
from propagate import propagate

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scc', type=str, default='', help='Five-digit NORAD ID')
    parser.add_argument('--predict', type=int, default=14, help='Number of days to propagate out to')
    parser.add_argument('--time_step', type=int, default=24, help='Time step in hours for propagation')
    parser.add_argument('--csv', type=bool, default=False, help='Output preprocessed data to CSV')
    args = parser.parse_args()

    # Preprocess ELSET
    if args.csv:
        if not Path('./data/preprocessed').exists():
            Path('./data/preprocessed').mkdir()
        preprocess(args.scc)

    # # Propagate TLE
    # propagate(args.scc, args.predict, args.time_step)