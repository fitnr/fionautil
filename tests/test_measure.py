#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

from unittest import TestCase as PythonTestCase
import unittest.main
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
        self.assertEqual(measure.azimuth(0, 0, 0, 0, clockwise=True, latlong=False), 0)
        self.assertEqual(measure.azimuth(1, 0, 0, 1, clockwise=True, latlong=False), -45)
        self.assertEqual(measure.azimuth(0, 1, 1, 0, clockwise=True, latlong=False), 135)
        self.assertEqual(measure.azimuth(0, 0, 0, 1, clockwise=True, latlong=False), 0)
        self.assertEqual(measure.azimuth(0, 0, 1, 0, clockwise=False, latlong=False), -90)
        self.assertEqual(measure.azimuth(1, 0, 0, 0, clockwise=True, latlong=False), 270)

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
        self.assertEqual(measure.azimuth_distance(1, 0, 0, 0, latlong=False), (-270, 1))


if __name__ == '__main__':
    unittest.main()
