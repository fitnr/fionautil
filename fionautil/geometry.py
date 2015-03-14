from itertools import chain
import math
import pyproj

def _transform_line(in_proj, out_proj, ring):
    xs, ys = pyproj.transform(in_proj, out_proj, *zip(*ring))  # pylint: disable=W0632
    return zip(xs, ys)


def _transform_multi(in_proj, out_proj, coordinates):
    return [transform_line(in_proj, out_proj, ring) for ring in coordinates]


def explode(geometry):
    '''A generator that returns every coordinate of every segment of a geometry'''
    if len(geometry['coordinates']) > 1:
        geomchain = chain(*geometry['coordinates'])
    else:
        geomchain = geometry['coordinates']

    # polygon is a list of tuples:
    # [(7.08545983, 53.686), (6.873789, 53.672), (6.9108, 53.683), (7.04704, 53.694), (7.085, 53.68699)]
    for polygon in geomchain:
        for point in polygon:
            yield point


def reproject(in_proj, out_proj, geometry):
    '''Transform a Fiona/GeoJSON geometry into another projection'''
    if geometry['type'] in ('MultiLineString', 'MultiPolygon'):
        coords = _transform_multi(in_proj, out_proj, geometry['coordinates'])

    elif geometry['type'] in ('LineString', 'Polygon'):
        coords = _transform_line(in_proj, out_proj, geometry['coordinates'])

    elif geometry['type'] == 'Point':
        coords = pyproj.transform(in_proj, out_proj, *geometry['coordinates'])

    return coords
