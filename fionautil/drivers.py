# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

import os.path
from fiona import supported_drivers

suffix_map = {
    'csv': 'CSV',
    'gdb': 'FileGDB',
    'dbf': 'ESRI Shapefile',
    'shp': 'ESRI Shapefile',
    'gtm': 'GPSTrackMaker',
    'dgn': 'DGN',
    'json': 'GeoJSON',
    'geojson': 'GeoJSON',
    'gpkg': 'GPKG',
    'mapinfo': 'MapInfo File',
    'gpx': 'GPX',
    'dxf': 'DXF',
    'bna': 'BNA',
    'gmt': 'GMT',
}


def from_path(path):
    _, suffix = os.path.splitext(os.path.basename(path))
    return from_suffix(suffix)


def from_suffix(suffix):
    '''Attempt to return the name of the appropriate GDAL driver, given a suffix.'''

    if suffix.startswith('.'):
        suffix = suffix[1:]

    if suffix in suffix_map and suffix_map[suffix] in supported_drivers:
        return suffix_map[suffix]

    return None
