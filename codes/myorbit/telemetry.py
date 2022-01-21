from skyfield.api import Loader, load
import os
from pathlib import Path

_tle_dir = os.environ.get('TLE_DIR', Path.home())
_tle_filename = 'iss.tle'
_tle_url = 'http://celestrak.com/NORAD/elements/stations.txt'

_timescale = load.timescale()

def load_iss():
    """
    Retrieves ISS telemetry data from a local or remote TLE file and
    returns a Skyfiled EarthSatellite object corresponding to the ISS.
    """
    loader = Loader(_tle_dir, verbose=False)
    try:
        # find telemetry data locally
        satellites = loader.tle_file(_tle_filename)
    except FileNotFoundError:
        pass
    else:
        iss = next((sat for sat in satellites if sat.name=='ISS (ZARYA)'), None)
        if iss is None:
            raise RuntimeError(f'Unable to retrieve ISS TLE data from {loader.path_to(_tle_filename)}')
        return iss
    
    try:
        # find telemetry data remotely
        satellites = loader.tle_file(_tle_url)
        Path(_tle_dir/Path(_tle_url).name).rename(_tle_dir/_tle_filename)
    except:
        pass
    else:
        iss = next((sat for sat in satellites if sat.name=='ISS (ZARYA)'), None)
        if iss is None:
            raise RuntimeError(f'Unable to retrieve ISS TLE data from {_tle_url}')
        return iss
    
    raise FileNotFoundError(f'Unable to retrieve ISS TLE data: cannot find{loader.path_to(_tle_filename)} or download {_tle_url}.')

def coordinates(satellite):
    """
    Return a Skyfield GeographicPosition object corresponding to the Earth
    latitude and longitude beneath the current celestial position of the ISS.
    
    See: rhodesmill.org/skyfield/api-topos.html#skyfield.toposlib.GeographicPosition
    """
    return satellite.at(_timescale.now()).subpoint()


# create ISS as a Skyfield EarthSatellite object
# See: rhodesmill.org/skyfield/api-satellite.html#skyfield.sgp4lib.EarthSatellite
ISS = load_iss()

# blind the coordinates function to the ISS object as a method
setattr(ISS, "coordinates", coordinates.__get__(ISS, ISS.__class__))