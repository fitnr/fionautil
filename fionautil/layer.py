import itertools
import fiona


def ffilter(func, filename):
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            return itertools.ifilter(func, layer)


def fmap(filename, func):
    '''Add properties to a fiona layer as its read.
    prop_func takes the feature as an argument and should return it with edited properties/geometry'''
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            return itertools.imap(func, layer)


def freduce(filename, func, initializer=None):
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
