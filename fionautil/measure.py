import math
import pyproj

WGS84 = pyproj.Geod(ellps='WGS84')


def distance(x0, y0, x1, y1, latlong=True):
    '''distance (in m) between two pairs of points'''
    if latlong:
        _, _, d = WGS84.inv(x0, y0, x1, y1)
    else:
        d = math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
    return d


def _projected_azimuth(x0, y0, x1, y1):
    '''The angle of a line between two points on a cartesian plane. Always clockwise and in degrees'''
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


def azimuth(x0, y0, x1, y1, radians=False, clockwise=None, latlong=True):
    '''azimuth between 2 geographic points'''
    if latlong:
        # this is always in angles
        az, _, _ = WGS84.inv(x0, y0, x1, y1)
    else:
        az = _projected_azimuth(x0, y0, x1, y1)

    if radians:
        az = math.radians(az)

    return az * (1 if clockwise else -1)


def signed_area(coords):
    """Return the signed area enclosed by a ring using the linear time
    algorithm at http://www.cgafaq.info/wiki/Polygon_Area. A value >= 0
    indicates a counter-clockwise oriented ring."""

    try:
        xs, ys = map(list, zip(*coords))
    except ValueError:
        # Attempt to handle a z-dimension
        xs, ys, _ = map(list, zip(*coords))

    xs.append(xs[1])
    ys.append(ys[1])
    return sum(xs[i] * (ys[i + 1] - ys[i - 1]) for i in range(1, len(coords))) / 2.0


def clockwise(coords):
    return signed_area(coords) < 0


def counterclockwise(coords):
    return signed_area(coords) >= 0


def azimuth_distance(x0, y0, x1, y1, latlong=True):
    '''Azimuth and distance between two points'''
    if latlong:
        az, _, dist = WGS84.inv(x0, y0, x1, y1)
    else:
        az = azimuth(x0, y0, x1, y1, latlong=latlong)
        dist = distance(x0, y0, x1, y1, latlong=latlong)

    return az, dist
