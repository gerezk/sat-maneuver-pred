import satkit
import math
import pandas as pd

def to_sma(mean_motion):
    """ Convert mean_motion (revs/day) to sma (km)
    Parameters
    ----------
    mean_motion : float
        Satellite's revs/day, extracted from TLE
    """
    mean_motion_rad_per_sec = mean_motion * (1.0 / 86400.0) * (2. * math.pi / 1.0)
    return (satkit.consts.GM**(1./3.) / mean_motion_rad_per_sec**(2./3.)) / 1000

class Preprocess:
    def __init__(self, args):
        self.args = args
        self.generate_csv()

    def generate_csv(self):
        catalog = satkit.TLE.from_file(f'data/TLE/{self.args.scc}.tle')

        # initialize dataframe
        headers = ['epoch',
                   'SMA (km)',
                   'eccentricity',
                   'inclination (deg)',
                   'arg of perigee (deg)',
                   'mean anomaly (deg)',
                   'maneuvered']
        df = pd.DataFrame(columns=headers)
        # get COEs from TLEs
        # RAAN missing for now since satkit doesn't have a RAAN property
        for TLE in catalog:
            epoch = TLE.epoch
            sma = to_sma(TLE.mean_motion)
            eccen = TLE.eccen
            inclination = TLE.inclination
            arg_of_perigee = TLE.arg_of_perigee
            mean_anomaly = TLE.mean_anomaly

            # append COEs from TLE to df using a dict
            # could be more efficient to create dict with all TLE data first then convert to df
            temp = {}
            data = [epoch, sma, eccen, inclination, arg_of_perigee, mean_anomaly]
            for i in range(len(data)):
                temp[headers[i]] = [data[i]]
            data = pd.DataFrame(temp)
            df = pd.concat([df, data], ignore_index=True)

        df.to_csv(f'data/preprocessed/{self.args.scc}.csv', index=False)

    def get_maneuver_dates(self, scc):
        """
        Get list of maneuver dates for given scc#
        :param scc:
        :return maneuver_dates:
        """
        pass