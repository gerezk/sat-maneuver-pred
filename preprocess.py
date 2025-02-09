import satkit
import math
import pandas as pd

def to_sma(mean_motion):
    """
    Convert mean_motion (revs/day) to sma (km)
    :param mean_motion:
    :return sma:
    """
    mean_motion_rad_per_sec = mean_motion * (1.0 / 86400.0) * (2. * math.pi / 1.0)
    return (satkit.consts.GM**(1./3.) / mean_motion_rad_per_sec**(2./3.)) / 1000

catalog = satkit.TLE.from_file('data/TLE/41335.tle')

# initialize pandas dataframe
headers = ['epoch',
           'SMA (km)',
           'eccentricity',
           'inclination (deg)',
           'arg of perigee (deg)',
           'mean anomaly (deg)']
df = pd.DataFrame(columns=headers)
# get COEs from TLEs and append to df
# RAAN missing for now since satkit doesn't have a RAAN property
dictionary_list = []
for TLE in catalog:
    epoch = TLE.epoch
    sma = to_sma(TLE.mean_motion)
    eccen = TLE.eccen
    inclination = TLE.inclination
    arg_of_perigee = TLE.arg_of_perigee
    mean_anomaly = TLE.mean_anomaly

    data = [epoch, sma, eccen, inclination, arg_of_perigee, mean_anomaly]
    for i in range(len(data)):
        dictionary_list.append({headers[i]: data[i]})

df_final = pd.DataFrame.from_dict(dictionary_list)
df_final.to_csv('data/preprocessed/41335.csv', index=False)