from itertools import chain
import pyproj
from . import measure


def endpoints(geometry):
    '''Return the first and last coordinates of a LineString or Multilinestring'''
    coords = geometry['coordinates']

    if geometry['type'] == 'MultiLineString':
        return coords[0][0], coords[-1][-1]

    elif geometry['type'] == 'LineString':
        return coords[0], coords[-1]

    raise ValueError("Improper Feature type.")


def startpoint(geometry):
    start, _ = endpoints(geometry)
    return start


def endpoint(geometry):
    _, end = endpoints(geometry)
    return end

def bbox(geometry):
    x, y = zip(*list(explode(geometry['coordinates'])))
    return min(x), min(y), max(x), max(y)


def azimuth(geometry, projection=None, radians=False, clockwise=False):
    '''return the azimuth of a fiona LineString given a feature and a Proj instance (or note that it's cartesian-ish'''

    if geometry['type'] not in ('LineString', 'MultiLineString'):
        raise ValueError("This only works with PolyLine layers, this is: {}".format(geometry['type']))

    first, last = endpoints(geometry)
    latlong = projection.is_latlong()

    if latlong:
        x0, y0 = projection(*first, inverse=True)
        x1, y1 = projection(*last, inverse=True)

    else:
        x0, y0 = first
        x1, y1 = last

    return measure.azimuth(x0, y0, x1, y1, radians=radians, clockwise=clockwise, latlong=latlong)


def disjointed(shapes):
    '''Reduce a list of shapely shapes to those that are disjoint from the others'''
    newshapes = [shapes[0]]
    for shape in shapes[1:]:
        for i, other in enumerate(newshapes):
            if shape.intersects(other):
                newshapes[i] = other.union(shape)
                break

    return newshapes

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


def explodelinestring(geometry):
    '''A generator that returns every line segment of every linestring'''

    if len(geometry['coordinates']) > 1:
        coords = chain(*geometry['coordinates'])
    else:
        coords = geometry['coordinates']

    for ring in coords:
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
