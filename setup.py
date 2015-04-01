#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

from setuptools import setup, find_packages
from fionautil import __version__

setup(
    name='fionautil',
    version=__version__,
    description='helpful utilities for working with geodata with Fiona',
    long_description='readme.rst',
    keywords='GIS',
    author='Neil Freeman',
    author_email='contact@fakeisthenewreal.org',
    url='http://github.com/fitnr/fionautil/',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'pyproj>=1.9.3,<1.10',
        'fiona>=1.5.0,<2.0',
        'shapely>=1.5.0,<2.0',
    ],

    test_suite='tests',

    use_2to3=True,

    tests_require=[
        'tox'
    ],

)
