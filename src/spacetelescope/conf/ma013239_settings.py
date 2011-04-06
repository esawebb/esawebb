# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from default_settings import *

ADMINS = (
	('Lars Holm Nielsen','lnielsen@eso.org'),
)

LOGGING_HANDLER = ['console']

##################
# DATABASE SETUP #
##################
#DATABASES['default']['USER'] = "spacetelescope"
#DATABASES['default']['HOST'] = "mysql1.hq.eso.org"
#DATABASES['default']['PASSWORD'] = "letoveumtold"

###############
# MEDIA SETUP #
###############
#MEDIA_ROOT = "/Volumes/webdocs/hubble/docs/static"

##########
# CACHE  #
##########
#CACHES = { 'default': { 'BACKEND': 'django.core.cache.backends.dummy.DummyCache', } }

##########	
# CELERY #
##########
BROKER_HOST = "localhost"
#BROKER_HOST = "aweb26.hq.eso.org"