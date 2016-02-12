#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

from unittest import TestCase as PythonTestCase
import unittest.main
from fionautil import coords

class TestCoords(PythonTestCase):

    def setUp(self):
        self.coords = [(1, 1), (-2, 2), (3, 14), (10, -1)]

    def testMinX(self):
        assert coords.min_x(self.coords) == -2

    def testMinY(self):
        assert coords.min_y(self.coords) == -1

    def testMaxX(self):
        assert coords.max_x(self.coords) == 10

    def testMaxY(self):
        assert coords.max_y(self.coords) == 14

    def test_segmentize(self):
        segments = coords.segmentize(self.coords)

        self.assertEqual(next(segments), ((1, 1), (-2, 2)))
        self.assertEqual(next(segments), ((-2, 2), (3, 14)))

    def test_bounds(self):
        assert coords.bounds(self.coords) == (-2, -1, 10, 14)

    def test_cornerbounds(self):
        b = (0, 0, 6, 8)
        self.assertSequenceEqual(coords.cornerbounds(b), [(0, 0), (0, 8), (6, 8), (6, 0)])

if __name__ == '__main__':
    unittest.main()
