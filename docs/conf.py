# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

import sys, os, datetime

from djangoplicity.sphinxconf import *

# General substitutions.
project = 'spacetelescope.org'
copyright = '2010-%s European Southern Observatory & European Space Agency' % current_year 

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.
version = read_version()
# The full version, including alpha/beta/rc tags.
release = version

# Output file base name for HTML help builder.
htmlhelp_basename = 'spacetelescopedoc'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = [
  ('index', 'spacetelescope.tex', 'Documentation for spacetelescope.org', 'European Southern Observatory \& European Space Agency', 'manual'),
]
