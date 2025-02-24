import orekit
vm = orekit.initVM()
from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir(from_pip_library=True)  # Sets up the data path (e.g., Orekit-data.zip)

# Import necessary Orekit classes
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from org.orekit.propagation import SpacecraftState
from org.orekit.orbits import OrbitType
from  org.orekit.propagation.conversion import DSSTPropagatorBuilder
from org.orekit.frames import FramesFactory
from org.orekit.time import AbsoluteDate

import pandas as pd
from pathlib import Path

def propagate(scc, predict, time_step):
    """ propagate a TLE out to predict
    :param scc: str
    :param predict: int (days)
    :param time_step: int (hours)
    :return: df of
    """
    tle = get_last_tle(scc)
    tle = TLE(tle[0], tle[1])
    tle_date = tle.getDate()

    # compute orbit from TLE using SGP4
    eme2000 = FramesFactory.getEME2000()
    propagator = TLEPropagator.selectExtrapolator(tle, eme2000) # DSST works best in inertial frame
    orbit = propagator.propagate(tle_date).getOrbit()
    SState = SpacecraftState(orbit)
    # keplerian = OrbitType.KEPLERIAN.convertType(orbit)

    # propagator = DSSTPropagatorBuilder(tle)

# write function to transform TLE to keplerian elements independent of SGP4

def get_last_tle(scc):
    """ Extract most recent TLE from a json containing ELSET data
    :param scc: str
    :return: list containing TLE
    """
    df = pd.read_json(Path(f'data/ELSET/{scc}.json'), convert_dates=['EPOCH'])
    tle = df[['TLE_LINE1', 'TLE_LINE2']].iloc[[-1]]
    return tle.values.tolist()[0]