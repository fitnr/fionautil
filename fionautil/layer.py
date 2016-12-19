# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

import itertools
from functools import reduce
import sys
import fiona
import fiona.transform

try:
    from shapely.geometry import mapping, shape as shapelyshape
except ImportError:
    pass
from .geometry import disjointed
from . import drivers


def meta(filename):
    '''Return crs and schema for a layer'''
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            return layer.meta


def meta_complete(filename):
    '''Return crs and schema for a layer, as well as additional metadata.'''
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            m = {
                'bounds': layer.bounds,
                'path': layer.path,
                'name': layer.name,
                'encoding': layer.encoding
            }
            m.update(layer.meta)
            return m


def bounds(filename):
    '''Shortcut for returning bounds of a layer (minx, miny, maxx, maxy)'''
    with fiona.drivers():
        with fiona.open(filename, 'r') as layer:
            return layer.bounds


def first(filename):
    '''Return the first feature of a layer'''
    with fiona.drivers():
        with fiona.open(filename, 'r') as layer:
            return next(layer)


def fiter(filename):
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            for feature in layer:
                yield feature


def _fionaiter(iterfunc):
    def _iter(func, filename, *args, **kwargs):
        with fiona.drivers():
            with fiona.open(filename, "r") as layer:
                for feature in iterfunc(func, layer, *args, **kwargs):
                    yield feature
    return _iter


@_fionaiter
def ffilter(func, layer, *args, **kwargs):
    return iter(f for f in layer if func(f, *args, **kwargs))


@_fionaiter
def ffilterfalse(func, layer, *args, **kwargs):
    return iter(f for f in layer if not func(f, *args, **kwargs))


@_fionaiter
def fmap(func, layer, *args, **kwargs):
    '''Yield features in a fiona layer, applying func to each'''
    return iter(func(f, *args, **kwargs) for f in layer)


def freduce(func, filename, initializer=None):
    '''Reduce features of a layer to a single value'''
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            return reduce(func, layer, initializer)


def fchain(*filenames):
    '''Reduce features of a layer to a single value'''
    for filename in itertools.chain(filenames):
        with fiona.drivers():
            with fiona.open(filename, "r") as layer:
                for feature in layer:
                    yield feature


def fslice(filename, start, stop=None, step=None):
    if stop is None:
        stop = start
        start = None

    it = iter(range(start or 0, stop or sys.maxsize, step or 1))
    nexti = next(it)

    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            for i, element in enumerate(layer):
                if i == nexti:
                    yield element
                    nexti = next(it)


def fzip(*filenames):
    with fiona.drivers():
        try:
            handles = [fiona.open(f) for f in filenames]
            for features in zip(*handles):
                yield features

        finally:
            for h in handles:
                h.close()


def shapes(filename, crs=None):
    '''
    Generator that yields a Shapely shape for every feature in a layer.
    '''
    try:
        shapelyshape
    except NameError:
        raise NotImplementedError("length require shapely")

    with fiona.drivers():
        with fiona.open(filename, 'r') as layer:
            if crs is not None:
                def _geom(feature):
                    return fiona.transform.transform_geom(layer.crs, crs, feature['geometry'])
            else:
                def _geom(feature):
                    return feature['geometry']

            for feature in layer:
                yield shapelyshape(_geom(feature))


def length(filename, crs=None):
    '''Get the length of a geodata file in its
    native projection or the given crs mapping'''
    geometries = shapes(filename, crs)
    return sum(x.length for x in geometries)


def perimeter(filename, crs=None):
    '''Get perimeter of all features in a geodata file in its
    native projection or the given crs mapping'''
    geometries = shapes(filename, crs)
    return sum(x.boundary.length for x in geometries)


def find(filename, key, value):
    '''Special case of ffilter: return the first feature where key==value'''
    def test(f):
        return f['properties'][key] == value
    return next(ffilter(test, filename))


def dissolve(sourcefile, sinkfile, key, unsplit=None):
    try:
        shape
    except NameError:
        raise NotImplementedError("dissolve require shapely")

    with fiona.drivers():
        with fiona.open(sourcefile) as source:
            schema = source.schema
            schema['properties'] = {key: source.schema['properties'][key]}

            with fiona.open(sinkfile, 'w', crs=source.crs, schema=schema, driver=source.driver) as sink:

                gotkeys = dict()

                for _, feat in source.items():
                    fkey = feat['properties'][key]
                    fshape = shapelyshape(feat['geometry'])

                    if fkey in gotkeys:
                        gotkeys[fkey][0] = gotkeys[fkey][0].union(fshape)
                    else:
                        gotkeys[fkey] = [fshape]

                for shapelist in gotkeys.values():
                    if unsplit:
                        for s in disjointed(shapelist):
                            sink.write(s)

                    else:
                        sink.write(shapelist[0])


def create(output, geometries, properties=None, crs=None, driver=None):
    '''
    Create a layer from a set of shapely geometries or geometry
    dicts. Use list of properties (dict) if provided, otherwise an index of list as an ID.'''
    try:
        schema = {'geometry': geometries[0].type}
    except AttributeError:
        schema = {'geometry': geometries[0]['type']}

    driver = driver or drivers.from_path(output)

    FIELD_MAP = {v: k for k, v in fiona.FIELD_TYPES_MAP.items()}

    if properties:
        schema['properties'] = {k: FIELD_MAP[type(v)] for k, v in properties[0].items()}
    else:
        schema['properties'] = {'id': 'int'}
        properties = [{'id': x} for x in range(len(geometries))]

    with fiona.drivers():
        with fiona.open(output, 'w', driver=driver, crs=crs, schema=schema) as f:
            for geom, props in zip(geometries, properties):
                try:
                    feature = {'properties': props, 'geometry': mapping(geom)}
                except AttributeError:
                    feature = {'properties': props, 'geometry': geom}

                f.write(feature)
