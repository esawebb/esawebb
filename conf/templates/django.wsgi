# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

import os, sys

# Redirect output to stderr so we don't get errors with print statements
sys.stdout = sys.stderr

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = '{{SETTINGS_MODULE}}'
os.environ['DJANGOPLICITY_SETTINGS'] = '{{LOCAL_SETTINGS_MODULE}}'
os.environ["CELERY_LOADER"] = "django"

# Load Django
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
