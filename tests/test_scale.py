#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

from unittest import TestCase as PythonTestCase
import unittest.main
from fionautil import scale
try:
    import numpy as np
except ImportError:
    pass


class TestCoords(PythonTestCase):

    def setUp(self):
        self.coords = [(1, 1), (-2, 2), (3, 14), (10, -1)]
        self.coordsx2 = [(2, 2), (-4, 4), (6, 28), (20, -2)]

    def test_scale(self):
        result = scale.scale(self.coords, 2)

        try:
            arr = np.array(self.coordsx2, dtype=float).tolist()
            result = result.tolist()
            self.assertEqual(result, arr)

        except NameError:
            self.assertEqual(list(result), self.coordsx2)


if __name__ == '__main__':
    unittest.main()
