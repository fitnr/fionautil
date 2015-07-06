from __future__ import print_function
import itertools
import fiona
import sys
from pyproj import Proj
from .geometry import disjointed
from shapely.geometry import shape


def meta(filename):
    '''Return crs and schema for a layer'''
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            return layer.meta


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
    def _iter(func, filename, *args):
        with fiona.drivers():
            with fiona.open(filename, "r") as layer:
                for feature in iterfunc(func, layer, *args):
                    yield feature
    return _iter


@_fionaiter
def ffilter(func, layer):
    return iter(f for f in layer if func(f))


@_fionaiter
def ffilterfalse(func, layer):
    return iter(f for f in layer if not func(f))


@_fionaiter
def fmap(func, layer):
    '''Yield features in a fiona layer, applying func to each'''
    return iter(func(f) for f in layer)


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


def length(filename, proj=None):
    '''Get the length of a geodata file in its
    native projection or the given Proj object'''

    with fiona.drivers():
        with fiona.open(filename, 'r') as layer:
            if not proj:
                proj = Proj(*layer.crs)

            return sum(shape({'type': feature['geometry']['type'],
                              'coordinates': zip(*proj(*feature['geometry']['coordinates']))}).length
                       for feature in layer)


def perimeter(filename, proj=None):
    '''Get perimeter of all features in a geodata file in its
    native projection or the given Proj object'''

    with fiona.drivers():
        with fiona.open(filename, 'r') as layer:
            if not proj:
                proj = Proj(*layer.crs)

            return sum(shape({'type': feature['geometry']['type'],
                              'coordinates': zip(*proj(*feature['geometry']['coordinates']))}).boundary.length
                       for feature in layer)


def find(filename, key, value):
    '''Special case of ffilter: return the first feature where key==value'''
    test = lambda f: f['properties'][key] == value
    return next(ffilter(test, filename))


def dissolve(sourcefile, sinkfile, key, unsplit=None):
    with fiona.drivers():
        with fiona.open(sourcefile) as source:
            schema = source.schema
            schema['properties'] = {key: source.schema['properties'][key]}

            with fiona.open(sinkfile, 'w', crs=source.crs, schema=schema, driver=source.driver) as sink:

                gotkeys = dict()

                for _, feat in source.items():
                    fkey = feat['properties'][key]
                    fshape = shape(feat['geometry'])

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
