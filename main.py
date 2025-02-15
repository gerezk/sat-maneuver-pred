import argparse
from pathlib import Path

from preprocess import preprocess, get_tle
from propagate import propagate

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scc', type=str, default='', help='Five-digit NORAD ID')
    parser.add_argument('--predict', type=int, default=14, help='Number of days to propagate out to')
    parser.add_argument('--csv', type=bool, default=False, help='Output preprocessed data to CSV')
    args = parser.parse_args()

    # Preprocess ELSET
    if not Path('./data/preprocessed').exists():
        Path('./data/preprocessed').mkdir()
    historical_ELSET = preprocess(args.scc, args.csv)

    # Propagate TLE
    propagate(args.scc, args.predict)