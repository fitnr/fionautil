#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

from unittest import TestCase as PythonTestCase
import unittest.main
from functools import partial
from math import pi
from os import path
from fionautil import measure
import fionautil.layer

shp = path.join(path.dirname(__file__), 'fixtures/testing.shp')


class TestMeasure(PythonTestCase):

    def testDistance(self):
        assert measure.distance(1, 0, 0, 0, False) == 1
        self.assertEqual(measure.distance(0, 0, 360, 0, True), 0.0)
        self.assertEqual(measure.distance(0, 0, 6, 0, True), 667916.9447596414)

    def testAzimuth(self):
        self.assertEqual(measure.azimuth(0, 0, 0, 0, clockwise=True, longlat=False), 0)
        self.assertEqual(measure.azimuth(1, 0, 0, 1, clockwise=True, longlat=False), -45)
        self.assertEqual(measure.azimuth(0, 1, 1, 0, clockwise=True, longlat=False), 135)
        self.assertEqual(measure.azimuth(0, 0, 0, 1, clockwise=True, longlat=False), 0)
        self.assertEqual(measure.azimuth(0, 0, 1, 0, clockwise=False, longlat=False), -90)
        self.assertEqual(measure.azimuth(1, 0, 0, 0, clockwise=True, longlat=False), 270)

        self.assertEqual(measure.azimuth(0, 0, 0, 90), -0.0)
        self.assertEqual(measure.azimuth(0, 0, 90, 0), -90.0)
        self.assertEqual(measure.azimuth(0, 0, 90, 0, radians=True), pi / -2)

    def testSignedArea(self):
        feature = fionautil.layer.first(shp)
        self.assertEqual(measure.signed_area(feature['geometry']['coordinates'][0]), -4.428726877457176)

        coords = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
        assert measure.signed_area(coords) == 1.0

        assert measure.clockwise(coords) == False
        assert measure.counterclockwise(coords) == True

        coords.reverse()

        assert measure.signed_area(coords) == -1.0
        assert measure.clockwise(coords) == True
        assert measure.counterclockwise(coords) == False

        zcoords = [(0, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)]
        assert measure.signed_area(zcoords) == 1.0

    def testAzimuthDistance(self):
        self.assertEqual(measure.azimuth_distance(0, 0, 90, 0), (90, 10018754.171394622))
        self.assertEqual(measure.azimuth_distance(1, 0, 0, 0, longlat=False), (-270, 1))

    def testDet(self):
        assert measure.det((1, 2), (3, 4)) == -2
        assert measure.det((3, 4), (1, 2)) == 2
        assert measure.det((100, 4), (1, -100)) == -10004

    def testIntersectingbounds(self):
        a = (0, 0, 10, 10)
        b = (0, 0, 9, 9)
        c = (10, 10, 20, 20)

        assert measure.intersectingbounds(a, b) is True
        assert measure.intersectingbounds(a, c) is True
        assert measure.intersectingbounds(b, c) is False

    def testIntersection(self):
        a = ((0, 0), (10, 10))
        b = ((10, 0), (0, 10))
        c = ((0, 5), (10, 5))
        d = ((12, 100), (13, 102))
        e = (0, 0), (5, 5)

        f = ((0, 0), (10, 0))
        g = ((5, 0), (15, 0))

        h = ((0, 0), (0, 10))
        i = ((0, 5), (0, 15))

        j = ((11, 11), (12, 12))

        k = (4, 5), (10, 11)
        m = (10, 10), (0, 0)
        n = (0, 10), (10, 10)

        self.assertEqual(measure.intersect(a, b), (5, 5))
        self.assertEqual(measure.intersect(a, c), (5, 5))

        self.assertIn(measure.intersect(a, e), list(a) + list(e))
        assert measure.intersect(e, a) in list(a) + list(e)

        assert measure.intersect(a, d) is None
        assert measure.intersect(b, d) is None

        assert measure.intersect(f, g) in list(f) + list(g)
        assert measure.intersect(g, f) in list(f) + list(g)

        assert measure.intersect(h, i) in list(h) + list(i)
        assert measure.intersect(i, h) in list(h) + list(i)

        assert measure.intersect(a, j) is None
        assert measure.intersect(k, m) is None
        assert measure.intersect(k, n) == (9, 10)

    def testIntersectionDet(self):
        minx, miny, maxx, maxy = 0, 0, 10, 10
        edges = (
            ((minx, miny), (minx, maxy)),
            ((minx, maxy), (maxx, maxy)),
            ((maxx, maxy), (maxx, miny)),
            ((maxx, miny), (minx, miny))
        )
        dets = [measure.det(*j) for j in edges]
        assert dets == [0, -100, -100, 0]

        a = (4, 5), (10, 11)
        assert measure.intersect(edges[0], a) is None
        assert measure.intersect(edges[1], a) == (9, 10)

        inters = [measure.intersect(e, a, detm=d) for e, d in zip(edges, dets)]
        self.assertListEqual(inters, [None, (9, 10), None, None])

    def testBoundsIntersect(self):
        intersect = partial(measure.intersectingbounds, (0, 0, 1, 1))

        assert intersect((0.5, 0.5, 1.5, 1.5)) is True
        assert intersect((-1, -1, 0.5, 0.5)) is True
        assert intersect((0, 0, 1, 1)) is True
        assert intersect((0, -1, 0, 1)) is True
        assert intersect((0.25, 1.25, 0.75, 1.75)) is False
        assert intersect((0.25, 0.25, 0.75, 0.75)) is True
        assert intersect((0.25, 0.25, 0.75, 4)) is True

if __name__ == '__main__':
    unittest.main()
