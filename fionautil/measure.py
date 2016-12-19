# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

import math

try:
    import pyproj
    WGS84 = pyproj.Geod(ellps='WGS84')
except ImportError:
    pass


def distance(x0, y0, x1, y1, longlat=True):
    '''distance (in m) between two pairs of points'''
    if longlat:
        try:
            _, _, d = WGS84.inv(x0, y0, x1, y1)
        except NameError:
            raise NotImplementedError("Distance of long/lat coordinates requires pyproj.")
    else:
        d = math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
    return d


def distance_points(p0, p1, longlat=True):
    '''distance (in m) between two points'''
    return distance(p0[0], p0[1], p1[0], p1[1], longlat)


def _projected_azimuth(x0, y0, x1, y1):
    '''The angle of a line between two points on a cartesian plane. Always clockwise and in degrees'''
    if y0 == y1:
        if x0 == x1:
            az = 0.
        elif x1 > x0:
            az = math.pi / 2.
        else:
            az = 3 * math.pi / 2.
    else:
        az = math.atan2((x1 - x0), (y1 - y0))

    return math.degrees(az)


def azimuth(x0, y0, x1, y1, radians=False, clockwise=None, longlat=True):
    '''
    Measure the azimuth between 2 geographic points

    Args:
        x0 (float): first x coordinate.
        y0 (float): first y coordinate.
        x1 (float): second x coordinate.
        y1 (float): second y coordinate.
        radians (bool): Return in radians.
        clockwise (bool): Return with clockwise coordinates.
        longlat (bool): Input is in longitude-latitude, rather than projected.

    Returns:
        float
    '''
    if longlat:
        # this is always in angles
        try:
            az, _, _ = WGS84.inv(x0, y0, x1, y1)
        except NameError:
            raise NotImplementedError("Distance of long/lat coordinates requires pyproj.")

    else:
        az = _projected_azimuth(x0, y0, x1, y1)

    if radians:
        az = math.radians(az)

    return az * (1 if clockwise else -1)


def azimuth_points(p0, p1, radians=False, clockwise=None, longlat=True):
    return azimuth(p0[0], p0[1], p1[0], p1[1], radians, clockwise, longlat)


def signed_area(coords):
    """Return the signed area enclosed by a ring using the linear time
    algorithm at http://www.cgafaq.info/wiki/Polygon_Area. A value >= 0
    indicates a counter-clockwise oriented ring."""

    try:
        xs, ys = tuple(map(list, zip(*coords)))
    except ValueError:
        # Attempt to handle a z-dimension
        xs, ys, _ = tuple(map(list, zip(*coords)))

    xs.append(xs[1])
    ys.append(ys[1])
    return sum(xs[i] * (ys[i + 1] - ys[i - 1]) for i in range(1, len(coords))) / 2.


def clockwise(coords):
    return signed_area(coords) < 0


def counterclockwise(coords):
    return signed_area(coords) >= 0


def azimuth_distance(x0, y0, x1, y1, longlat=True):
    '''Azimuth and distance between two points'''
    if longlat:
        try:
            az, _, dist = WGS84.inv(x0, y0, x1, y1)
        except NameError:
            raise NotImplementedError("Distance of long/lat coordinates requires pyproj.")

    else:
        az = azimuth(x0, y0, x1, y1, longlat=longlat)
        dist = distance(x0, y0, x1, y1, longlat=longlat)

    return az, dist


def azimuth_distance_points(p0, p1, longlat=True):
    return azimuth_distance(p0[0], p0[1], p1[0], p1[1], longlat)


def det(a, b):
    '''Determinant of a 2x2 matrix'''
    return a[0] * b[1] - a[1] * b[0]


def onsegment(segment, point):
    '''Return True if point lies on segment'''
    xs, ys = tuple(zip(*segment))
    pbr = point[0], point[1], point[0], point[1]

    if not intersectingbounds((min(xs), min(ys), max(xs), max(ys)), pbr):
        return False

    return (point[1] - ys[0]) * (xs[1] - xs[0]) == (ys[1] - ys[0]) * (point[0] - xs[0])


def intersectingbounds(mbr1, mbr2):
    '''Return True if two bounding boxes intersect, else False.'''
    # Check if intersection is impossible
    if mbr1[2] < mbr2[0] or mbr2[2] < mbr1[0] or mbr1[3] < mbr2[1] or mbr2[3] < mbr1[1]:
        return False
    else:
        return True


def coincidentendpoint(linem, linen):
    '''Assuming segments linem and linem, return an overlapping point'''
    if onsegment(linem, linen[0]):
        return linen[0]
    elif onsegment(linem, linen[1]):
        return linen[1]
    elif onsegment(linen, linem[0]):
        return linem[0]
    elif onsegment(linen, linem[1]):
        return linem[1]
    return None


def intersect(linem, linen, detm=None):
    '''
    Check if two line segments intersect. Returns None or the intersection.
    If lines are coincident, returns one of the midpoints.

    Args:
        linem (Sequence): line segment 1, e.g. ((0, 0), (1, 1))
        linen (Sequence): line segment 2, e.g. [[0, 1], [0, 1]]
        det (float): The determinant of linem. Precalculating might be useful if
                   calculating intersection with the same segment many times
    '''
    mx, my = tuple(zip(*linem))
    nx, ny = tuple(zip(*linen))

    mbrm = min(mx), min(my), max(mx), max(my)
    mbrn = min(nx), min(ny), max(nx), max(ny)

    if not intersectingbounds(mbrm, mbrn):
        return None

    xD = mx[0] - mx[1], nx[0] - nx[1]
    yD = my[0] - my[1], ny[0] - ny[1]

    div = det(xD, yD)

    if div == 0:
        try:
            # Check if lines are parallel
            if (xD[0] == xD[1] and yD[0] == yD[1]) or (yD[0] / xD[0] == yD[1] / float(xD[1])):
                return coincidentendpoint(linem, linen)

        except ZeroDivisionError:
            pass

        return None

    else:
        detm = detm or det(*linem)
        detn = det(*linen)
        x = det((detm, detn), xD) / float(div)
        y = det((detm, detn), yD) / float(div)

        if (intersectingbounds(mbrm, (x, y, x, y)) and
                intersectingbounds(mbrn, (x, y, x, y))):
            return x, y
        else:
            return None
