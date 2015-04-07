#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

import unittest
from fionautil import __version__


class VersionTestCase(unittest.TestCase):
    def test_has_proper_version(self):
        assert __version__ == '0.3.0'

