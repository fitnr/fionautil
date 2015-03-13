import fiona

def filter(filename, test):
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            for feature in layer:
                if test(feature):
                    yield feature


def mutate(filename, func):
    '''Add properties to a fiona layer as its read.
    prop_func takes the feature as an argument and should return it with edited properties/geometry'''
    with fiona.drivers():
        with fiona.open(filename, "r") as layer:
            for feature in layer:
                yield func(feature)

def find(filename, field, value):
    with fiona.drivers():
        with fiona.open(filename, "r") as source:
            for f in source:
                if f['properties'][field] == value:
                    return f
    raise KeyError('value not found for field: {}: {}'.format(field, value))
