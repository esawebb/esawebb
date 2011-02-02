# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

# Using distribute instead of setuptools
import distribute_setup
distribute_setup.use_setuptools()

import os
from setuptools import setup, find_packages

setup(
	name = 'spacetelescope',
	packages = find_packages('src'),
	package_dir = { '': 'src' },
	include_package_data = True,
	zip_safe = False,
)