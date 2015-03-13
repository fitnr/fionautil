import math
from .wgs84 import WGS84

def distance(x0, y0, x1, y1):
    '''distance (in m) between two (lon, lat) pairs'''
    _, _, d = WGS84.inv(x0, y0, x1, y1)
    return d


def azimuth(x0, y0, x1, y1, radians=True, **kwargs):
    '''azimuth between 2 geographic points'''
    if kwargs['projected']:
        if y0 == y1:
            if x0 == x1:
                az = 0
            elif x1 > x0:
                az = math.pi / 2
            else:
                az = 3 * math.pi / 2
        else:
            az = math.atan2((x1 - x0), (y1 - y0))

        if radians:
            return az
        else:
            return math.degrees(az)

    else:
        az, _, _ = WGS84.inv(x0, y0, x1, y1)

    if radians:
        return math.radians(az)
    else:
        return az

