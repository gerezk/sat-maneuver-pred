import orekit
vm = orekit.initVM()

from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir(from_pip_library=True)  # Sets up the data path (e.g., Orekit-data.zip)

def propagate(scc, predict):
    print('Hello')