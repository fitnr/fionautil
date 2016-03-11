# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

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
    return [_round(tuple(pt), precision) for pt in ring]


def geometry(geom, precision):
    g = dict(geom.items())

    if geom['type'] == 'GeometryCollection':
        g['geometries'] = [geometry(x, precision) for x in geom['geometries']]
        return g

    try:
        c = np.array(geom['coordinates'])
        g['coordinates'] = np.round(c, precision)

    except (AttributeError, KeyError, TypeError, NameError):

        if geom['type'] == 'Point':
            g['coordinates'] = _round(geom['coordinates'], precision)

        elif geom['type'] in ('MultiPoint', 'LineString'):
            g['coordinates'] = round_ring(geom['coordinates'], precision)

        elif geom['type'] in ('MultiLineString', 'Polygon'):
            g['coordinates'] = [round_ring(r, precision) for r in geom['coordinates']]

        elif geom['type'] == 'MultiPolygon':
            g['coordinates'] = [[round_ring(r, precision) for r in rings] for rings in geom['coordinates']]

    return g


def feature(feat, precision):
    feat['geometry'] = geometry(feat['geometry'], precision)
    return feat
