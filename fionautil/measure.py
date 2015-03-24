import math
from .wgs84 import WGS84


def distance(x0, y0, x1, y1):
    '''distance (in m) between two (lon, lat) pairs'''
    _, _, d = WGS84.inv(x0, y0, x1, y1)
    return d


def _projected_azimuth(x0, y0, x1, y1):
    '''The angle between two points on a cartesian plane. Always clockwise and in angles'''
    if y0 == y1:
        if x0 == x1:
            az = 0
        elif x1 > x0:
            az = math.pi / 2
        else:
            az = 3 * math.pi / 2
    else:
        az = math.atan2((x1 - x0), (y1 - y0))

    return math.degrees(az)


def azimuth(x0, y0, x1, y1, radians=False, clockwise=None, cartesian=None):
    '''azimuth between 2 geographic points'''
    if cartesian:
        az = _projected_azimuth(x0, y0, x1, y1)
    else:
        # this is always in angles
        az, _, _ = WGS84.inv(x0, y0, x1, y1)

    if radians:
        az = math.radians(az)

    return az * (1 if clockwise else -1)
