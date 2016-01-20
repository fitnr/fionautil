try:
    import numpy as np
except ImportError:
    pass

def _round(pt, precision):
    try:
        return round(pt[0], precision), round(pt[1], precision)
    except TypeError:
        pt = list(pt)
        return round(pt[0], precision), round(pt[1], precision)


def round_ring(ring, precision):
    try:
        np.round(coordinates, precision)
    except NameError:
        return [_round(pt, precision) for pt in ring]


def round_ringlist(coordinates, precision):
    # Drop possible Z coordinates and round. Two tracks here: numpy style and without-numpy style.
    try:
        return [np.round(np.array(ring)[:, 0:2], precision) for ring in coordinates]

    except NameError:
        return [round_ring(coordinates, precision) for ring in coordinates]


def geometry(geom, precision):
    if geom['type'] == 'Point':
        geom['coordinates'] = _round(geom['coordinates'], precision)

    elif geom['type'] in ('MultiPoint', 'LineString'):
        geom['coordinates'] = round_ring(geom['coordinates'], precision)

    elif geom['type'] in ('MultiLineString', 'Polygon'):
        geom['coordinates'] = round_ringlist(geom['coordinates'], precision)

    elif geom['type'] == 'MultiPolygon':
        geom['coordinates'] = [round_ringlist(r, precision) for r in geom['coordinates']]

    return geom

def feature(feat, precision):
    feat['geometry'] = geometry(feat['geometry'], precision)
    return feat
