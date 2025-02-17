import pandas as pd
import yaml
from pathlib import Path
import math

import orekit
vm = orekit.initVM()
from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir(from_pip_library=True)  # Sets up the data path (e.g., Orekit-data.zip)

# Import necessary Orekit classes
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from org.orekit.orbits import OrbitType, KeplerianOrbit
from org.orekit.frames import FramesFactory
from org.orekit.time import AbsoluteDate, TimeScalesFactory

def preprocess(scc):
    """ get corrected COEs by feeding TLE file into SGP4, then output COEs and TLE into a csv
    :param scc: str
    :return: nothing, outputs csv of preprocessed data for analysis and feeding into model
    """
    dict = {'epoch': [], # data loaded from TLEs into list values by key
            'sma (km)': [],
            'eccentricity': [],
            'inclination (deg)': [],
            'arg perigee (deg)': [],
            'raan (deg)': [],
            'mean anomaly (deg)': [],
            'TLE line 1': [],
            'TLE line 2': [],
            'maneuvered': []} # 1 = last TLE prior to a maneuver, 0 = no maneuver

    file = open(Path(f'data/tle/{scc}.tle'),'r')
    content = file.read().splitlines()
    for i in range(0, len(content)-1, 2):
        # get corrected COEs
        tle_line1 = content[i]
        tle_line2 = content[i+1]
        keplerian = get_keplerian_orbit(tle_line1, tle_line2)

        # append to lists in dict
        dict['epoch'].append(keplerian.getDate())
        dict['sma (km)'].append(keplerian.getA()/1000.)
        dict['eccentricity'].append(keplerian.getE())
        dict['inclination (deg)'].append(math.degrees(keplerian.getI()))
        dict['arg perigee (deg)'].append(math.degrees(keplerian.getPerigeeArgument()))
        dict['raan (deg)'].append(math.degrees(keplerian.getRightAscensionOfAscendingNode()))
        dict['mean anomaly (deg)'].append(math.degrees(keplerian.getMeanAnomaly()))
        dict['TLE line 1'].append(tle_line1)
        dict['TLE line 2'].append(tle_line2)

    # get maneuver data
    maneuvers = get_maneuvers(scc)
    maneuvers = [i for i in maneuvers if i.isAfter(dict['epoch'][0])] # remove timestamps prior to first ELSET

    # add column labeling if sat maneuvered following given ELSET
    # could be refactored so everything is done within the loop in line 35
    try:
        for index in range(len(dict['epoch'])):
            if maneuvers[0].isBetween(dict['epoch'][index], dict['epoch'][index + 1]) and len(maneuvers) > 0: # find ELSET immediately prior to maneuver
                dict['maneuvered'].append(1)
                maneuvers.pop(0)
            else:
                dict['maneuvered'].append(0)
    except IndexError: # reached last maneuver, fill rest of column with 0
        for index in range(len(dict['epoch']) - len(dict['maneuvered'])):
            dict['maneuvered'].append(0)

    df_final = pd.DataFrame.from_dict(dict)
    df_final.to_csv(Path(f'data/preprocessed/{scc}.csv'), index=False)

def get_maneuvers(scc):
    """ pull maneuver data from yaml and return as list of orekit AbsoluteDate instances
    :param scc: str
    :return: list of AbsoluteDate instances
    """
    with open(Path(f'data/maneuver_timestamps/{scc}.yaml'), 'r') as stream:
        content = yaml.load(stream, Loader=yaml.FullLoader)
    maneuvers = content['manoeuvre_timestamps']
    maneuvers_processed = []
    for i in maneuvers:
        orekit_date = AbsoluteDate(i.year,
                                   i.month,
                                   i.day,
                                   i.hour,
                                   i.minute,
                                   float(i.second),
                                   TimeScalesFactory.getUTC())
        maneuvers_processed.append(orekit_date)
    return maneuvers_processed

def get_last_tle(scc):
    """ Extract most recent TLE from a json containing ELSET data
    :param scc: str
    :return: list containing TLE
    """
    df = pd.read_json(Path(f'data/tle/{scc}.json'), convert_dates=['EPOCH'])
    tle = df[['TLE_LINE1', 'TLE_LINE2']].iloc[[-1]]
    return tle.values.tolist()[0]

def get_keplerian_orbit(tle_line1, tle_line2):
    """ Feed TLE into SGP4, then output KeplerianOrbit instance in the inertial frame
    :param tle_line1: str
    :param tle_line2: str
    :return: KeplerianOrbit instance
    """
    tle = TLE(tle_line1, tle_line2)
    eme2000 = FramesFactory.getEME2000()
    propagator = TLEPropagator.selectExtrapolator(tle, eme2000) # DSST works best in inertial frame
    orbit = propagator.propagate(tle.getDate()).getOrbit()
    orbit = OrbitType.KEPLERIAN.convertType(orbit) # returns only regular orbit
    return KeplerianOrbit.cast_(orbit) # cast to KeplerianOrbit