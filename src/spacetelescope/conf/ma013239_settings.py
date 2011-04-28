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
from djangoplicity.settings import copy_setting

ADMINS = (
	('Lars Holm Nielsen','lnielsen@eso.org'),
)

LOGGING_HANDLER = ['console']

##############
# DEPLOYMENT #
##############
DEPLOYMENT_EXISTING_CHECKOUT = "~/Workspaces/web/"

##################
# DATABASE SETUP #
##################
#DATABASES = copy_setting(DATABASES)
#DATABASES['default']['USER'] = "spacetelescope"
#DATABASES['default']['HOST'] = "mysql1i.hq.eso.org"
#DATABASES['default']['PASSWORD'] = "fivjeylvoked"

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