#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

from unittest import TestCase as PythonTestCase
import unittest.main
import os.path
import fionautil.layer

shp = os.path.join(os.path.dirname(__file__), 'fixtures/testing.shp')
geojson = os.path.join(os.path.dirname(__file__), 'fixtures/testing.geojson')


class TestLayer(PythonTestCase):

    def test_ffilter(self):
        test = lambda f: f['properties']['id'] == 3
        assert len(list(fionautil.layer.ffilter(test, shp))) == 1
        assert len(list(fionautil.layer.ffilter(test, geojson))) == 1

    def test_ffilterfalse(self):
        test = lambda f: f['properties']['id'] == 3
        assert len(list(fionautil.layer.ffilterfalse(test, shp))) == 3
        assert len(list(fionautil.layer.ffilterfalse(test, shp))) == 3

    def test_fmap(self):
        def func(f):
            f['properties']['cat'] = 'meow'
            return f

        assert next(fionautil.layer.fmap(func, shp)).get('properties').get('cat') == 'meow'
        assert next(fionautil.layer.fmap(func, geojson)).get('properties').get('cat') == 'meow'

    def test_freduce(self):
        def func(g, f):
            g = g or {'geometry': {'coordinates': []}}
            g['geometry']['coordinates'] = g['geometry']['coordinates'] + f['geometry']['coordinates']
            return g

        start = {
            'geometry': {
                'coordinates': []
            }
        }

        assert fionautil.layer.freduce(func, shp, start)
        assert fionautil.layer.freduce(func, geojson)
        assert len(fionautil.layer.freduce(func, shp, start).get('geometry').get('coordinates')) == 8

    def test_fchain(self):
        chain = fionautil.layer.fchain(shp, geojson)
        assert len(list(chain)) == 8

    def test_fslice(self):
        assert list(fionautil.layer.fslice(shp, 1, 2))
        assert list(fionautil.layer.fslice(geojson, 0, 4, 2))

    def test_fzip(self):
        assert list(fionautil.layer.fzip(shp, geojson))
        assert len(list(fionautil.layer.fzip(shp, geojson))) == 4
        assert type(next(fionautil.layer.fzip(shp, geojson))) == tuple

    def test_find(self):
        two = fionautil.layer.find(shp, 'id', 2)
        one = fionautil.layer.find(geojson, 'id', 1)
        assert one['properties']['id'] == 1
        assert two['properties']['id'] == 2


if __name__ == '__main__':
    unittest.main()
