# -*- coding: utf-8 -*-

"""Scale geometries and features."""

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

try:
    import numpy as np
except ImportError:
    pass


def geometry(geom, factor=1):
    g = dict(geom.items())

    if geom['type'] == 'MultiPolygon':
        g['coordinates'] = [scale_rings(rings, factor) for rings in geom['coordinates']]

    elif geom['type'] in ('Polygon', 'MultiLineString'):
        g['coordinates'] = scale_rings(geom['coordinates'], factor)

    elif geom['type'] in ('MultiPoint', 'LineString'):
        g['coordinates'] = scale(geom['coordinates'], factor)

    elif geom['type'] == 'Point':
        g['coordinates'] = scale(geom['coordinates'], factor)

    elif geom['type'] == 'GeometryCollection':
        g['geometries'] = [geometry(i) for i in geom['geometries']]

    else:
        raise NotImplementedError("Unknown geometry type")

    return g


def scale_rings(rings, factor=1):
    return [scale(ring, factor) for ring in rings]


def scale(coordinates, scalar=1):
    '''Scale a list of coordinates by a scalar. Only use with projected coordinates'''
    try:
        try:
            arr = np.array(coordinates, dtype=float)

        except TypeError:
            arr = np.array(list(coordinates), dtype=float)

        return arr * scalar

    except NameError:
        if isinstance(coordinates, tuple):
            return [coordinates[0] * scalar, coordinates[1] * scalar]

        return [(c[0] * scalar, c[1] * scalar) for c in coordinates]


def feature(feat, factor=1):
    return {
        'properties': feat.get('properties'),
        'geometry': geometry(feat['geometry'], factor),
    }
