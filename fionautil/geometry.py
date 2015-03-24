from itertools import chain
import math
import pyproj

from . import measure, rotation


def endpoints(geometry):
    '''Return the first and last coordinates of a LineString or Multilinestring'''
    coords = geometry['coordinates']

    if geometry['type'] == 'MultiLineString':
        return coords[0][0], coords[-1][-1]

    elif geometry['type'] == 'LineString':
        return coords[0], coords[-1]

    raise ValueError("Improper Feature type.")


def startpoint(feature):
    start, _ = endpoints(feature)
    return start


def endpoint(feature):
    _, end = endpoints(feature)
    return end


def azimuth(geometry, projection, radians=None):
    '''return the azimuth of a fiona LineString given a feature and a Proj instance'''

    if geometry['type'] not in ('LineString', 'MultiLineString'):
        raise ValueError("This only works with PolyLine layers, this is: {}".format(geometry['type']))

    first, last = endpoints(geometry)

    x0, y0 = projection(*first, inverse=True)
    x1, y1 = projection(*last, inverse=True)

    return measure.azimuth(x0, y0, x1, y1, radians=radians)


def rotate(geometry, angle=None, projected=None):
    '''rotate line feature. by default, endpoint will lie directly below start'''
    angle = angle or math.pi

    if geometry['type'] == 'LineString':
        newcoords = rotation.linestring(geometry['coordinates'], angle, projected=projected)

    elif geometry['type'] == 'MultiLineString':
        base = geometry['coordinates'][0][0]
        newcoords = [rotation.linestring(line, angle, base, projected=projected) for line in geometry['coordinates']]

    else:
        raise ValueError("Didn't recognize geometry type {}. {}".format(geometry['type'], geometry))

    geometry['coordinates'] = newcoords

    return geometry


def transform_line(in_proj, out_proj, ring):
    xs, ys = pyproj.transform(in_proj, out_proj, *zip(*ring))  # pylint: disable=W0632
    return zip(xs, ys)


def transform_multi(in_proj, out_proj, coordinates):
    return [transform_line(in_proj, out_proj, ring) for ring in coordinates]


def explode(geometry):
    '''A generator that returns every coordinate of every segment of a geometry'''
    for ring in geometry['coordinates']:
        for point in ring:
            yield point


def explodesegments(geometry):
    '''A generator that returns every line segment of every polygon in a geometry'''
    for ring in geometry['coordinates']:
        for i, point in enumerate(ring[:-1]):
            yield point, ring[i + 1]


def reproject(in_proj, out_proj, geometry):
    '''Transform a Fiona/GeoJSON geometry into another projection'''
    if geometry['type'] in ('MultiLineString', 'MultiPolygon'):
        coords = transform_multi(in_proj, out_proj, geometry['coordinates'])

    elif geometry['type'] in ('LineString', 'Polygon'):
        coords = transform_line(in_proj, out_proj, geometry['coordinates'])

    elif geometry['type'] == 'Point':
        coords = pyproj.transform(in_proj, out_proj, *geometry['coordinates'])

    return coords


def countpoints(geometry):
    return len(list(chain(*geometry['coordinates'])))


def countsegments(geometry):
    return countpoints(geometry) - 1


def flip(x, y):
    return y, x
