# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

try:
    from shapely.geometry import shape as shapelyshape
except ImportError:
    pass


def field_contains_test(field_values):
    '''
    Return a test function that checks if the properties of a feature match the possible values in field_values.

    >>> test = field_contains_test({'a': (1, 2, 3)})
    >>> test({'properties': {'a': 1}})
    True
    >>> test({'properties': {'a': 4}})
    False
    '''
    def test(feature):
        for k, v in field_values.items():
            if feature['properties'].get(k) not in v:
                return False
        return True

    return test


def togeojson(typ, coordinates, properties=None):
    '''Return a GeoJSON-ready object given a properties dict, a type and coordinates.'''
    properties = properties or {}

    return {
        'type': 'Feature',
        'properties': properties,
        'geometry': {
            'type': typ,
            'coordinates': coordinates,
        }
    }


def shape(feature):
    '''Applies shapely.geometry.shape to the geometry part of a feature
    and returns a new feature object with properties intact'''
    try:
        return {
            'properties': feature.get('properties'),
            'geometry': shapelyshape(feature['geometry'])
        }

    except NameError:
        raise NotImplementedError("shapify requires shapely")


def shapify(feature):
    '''Applies shapely.geometry.shape to the geometry part of a feature
    and returns a new feature object with properties intact'''
    return shape(feature)


def length(feature):
    '''Returns shapely length'''
    try:
        geom = shape(feature['geometry'])
        return geom.length

    except NameError:
        raise NotImplementedError("length requires shapely")


def compound(feature):
    '''Returns True if feature has more than one part:
    * A polygon with holes
    * A MultiPolygon or MultiLineString
    '''
    if 'Multi' in feature['geometry']['type']:
        return True

    if (feature['geometry']['type'] == 'Polygon' and
            len(feature['geometry']['coordinates']) > 1):
        return True

    return False
