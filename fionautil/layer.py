from __future__ import print_function
import itertools
import fiona
import sys
from .feature import shapify
from .geometry import disjointed

def meta(filename):
    '''Return crs and schema for a layer'''
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            return layer.crs, layer.schema


def bounds(filename):
    with fiona.drivers():
        with fiona.open(filename, 'r') as layer:
            return layer.bounds()

def first(filename):
    '''Return the first feature of a layer'''
    with fiona.drivers():
        with fiona.open(filename, 'r') as layer:
            return next(layer)


def fionaiter(iterfunc):
    def _iter(func, filename, *args):
        with fiona.drivers():
            with fiona.open(filename, "r") as layer:
                for feature in iterfunc(func, layer, *args):
                    yield feature
    return _iter


@fionaiter
def ffilter(func, layer):
    return iter(f for f in layer if func(f))


@fionaiter
def ffilterfalse(func, layer):
    return iter(f for f in layer if not func(f))


@fionaiter
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

    it = iter(xrange(start or 0, stop or sys.maxint, step or 1))
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
                    fshape = shapify(feat)

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

