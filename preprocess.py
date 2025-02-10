import pandas as pd
import yaml

class Preprocess:
    def __init__(self, args):
        self.args = args
        self.generate_csv()

    def generate_csv(self):
        # dump ELSET data from JSON into df
        df = pd.read_json(f'data/ELSET/{self.args.scc}.json', convert_dates=['EPOCH'])
        features = ['EPOCH',
                    'ECCENTRICITY',
                    'INCLINATION',
                    'RA_OF_ASC_NODE',
                    'ARG_OF_PERICENTER',
                    'SEMIMAJOR_AXIS',
                    'MEAN_ANOMALY']
        non_features = [i for i in list(df) if i not in features]
        df.drop(non_features, axis=1, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # extract maneuver data from yaml
        with open(f'data/maneuver_timestamps/{self.args.scc}.yaml', 'r') as stream:
            maneuvers = yaml.load(stream, Loader=yaml.FullLoader)
        maneuvers = maneuvers['manoeuvre_timestamps']
        maneuvers = [i for i in maneuvers if i > df['EPOCH'][0]] # remove timestamps prior to first ELSET

        # add column labeling if sat maneuvered following given ELSET
        maneuvered_feature = []
        try:
            for index in range(df.shape[0]):
                if  df['EPOCH'][index] < maneuvers[0] < df['EPOCH'][index + 1] and len(maneuvers) > 0: # find ELSET immediately prior to maneuver
                    maneuvered_feature.append(1)
                    maneuvers.pop(0)
                else:
                    maneuvered_feature.append(0)
        except IndexError: # reached last maneuver, fill rest of column with 0
            for index in range(df.shape[0] - len(maneuvered_feature)):
                maneuvered_feature.append(0)
        df['MANEUVERED'] = maneuvered_feature

        df.to_csv(f'data/preprocessed/{self.args.scc}.csv', index=False)