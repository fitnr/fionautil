#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

import unittest
import fionautil.round
try:
    import numpy as np
except ImportError:
    pass


class RoundTestCase(unittest.TestCase):

    def setUp(self):
        self.polygon = {
            "type": "Polygon",
            "coordinates": [
                [
                    [100.11111, 0.0],
                    [101.0, 0.11111],
                    [101.0, 1.11111],
                    [100.11111, 1.0],
                    [100.11111, 0.0]
                ]
            ]
        }

    def testRound(self):
        ring = [(10.00011111, 10.00011111), (10.00011111, 10.00011111)]
        round1 = fionautil.round._round(ring[0], 1)
        round2 = fionautil.round.round_ring(ring, 1)

        try:
            round1 = round1.tolist()
            round2 = round2[0].tolist()
        except AttributeError:
            round2 = round2[0]

        self.assertSequenceEqual(round1, (10.0, 10.0))
        self.assertSequenceEqual(round2, (10.0, 10.0))

    def testRoundPolygon(self):
        g = fionautil.round.geometry(self.polygon, 3)

        try:
            coordinates = g['coordinates'].tolist()
        except AttributeError:
            coordinates = g['coordinates']

        self.assertSequenceEqual(coordinates[0][0], [100.111, 0.0])

    def testRoundMultiPolygon(self):
        mp = {
            "type": "MultiPolygon",
            "coordinates": [self.polygon['coordinates'], self.polygon['coordinates']]
        }
        g = fionautil.round.geometry(mp, 3)

        try:
            coordinates = g['coordinates'][0][0][0].tolist()
        except AttributeError:
            coordinates = g['coordinates'][0][0][0]

        self.assertSequenceEqual(coordinates, [100.111, 0.0])

    def testRoundFeature(self):
        feat = {
            "geometry": self.polygon,
            "properties": {"foo": "bar"}
        }
        f = fionautil.round.feature(feat, 4)

        try:
            coordinates = f['geometry']['coordinates'][0][0].tolist()
        except AttributeError:
            coordinates = f['geometry']['coordinates'][0][0]

        self.assertSequenceEqual(coordinates, [100.1111, 0.0])
        assert f['properties']['foo'] == 'bar'

    def testRoundGenerator(self):
        x = (float(x) + 0.555 for x in range(2))
        b = fionautil.round._round(x, 2)

        try:
            b = b.tolist()
        except AttributeError:
            pass

        self.assertSequenceEqual(b, (0.56, 1.56))

    def testRoundListIfNumpy(self):
        try:
            np
        except NameError:
            return

        result = fionautil.round.geometry(self.polygon, 0)

        self.assertSequenceEqual(result['coordinates'][0][0].tolist(), [100.0, 0.0])

if __name__ == '__main__':
    unittest.main()
