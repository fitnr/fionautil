#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

from setuptools import setup, find_packages

try:
    readme = open('README.rst').read()
except IOError:
    readme = ''

shapely = 'shapely>=1.5.0,<2.0'

with open('fionautil/__init__.py') as i:
    version = next(r for r in i.readlines() if '__version__' in r).split('=')[1].strip('"\' \n')

setup(
    name='fionautil',
    version=version,
    description='helpful utilities for working with geodata with Fiona',
    long_description=readme,
    keywords='GIS',
    author='Neil Freeman',
    author_email='contact@fakeisthenewreal.org',
    url='http://github.com/fitnr/fionautil/',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fiona>=1.7.1,<2.0',
    ],

    extras_require={
        'shapify': [shapely],
        'shape': [shapely],
        'length': [shapely],
        'dissolve': [shapely],
        'speed': ['numpy>1.9'],
        'azimuth': ['pyproj>=1.9.5,<1.10'],
    },

    test_suite='tests',
)
