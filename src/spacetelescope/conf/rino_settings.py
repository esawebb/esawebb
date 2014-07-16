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
	('Bruno Rino','brino@partner.eso.org'),
)

#####################
# CONFIG GENERATION #
#####################
SHORT_NAME = 'hubble'
WEBSERVERS = ()
SSL_ASSETS_PREFIX = "www.spacetelescope.org"
CONFIG_GEN_TEMPLATES_DIR = "%s/conf/templates/" % PRJBASE
CONFIG_GEN_GENERATED_DIR = "%s/conf/" % TMP_DIR

SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"
CSRF_MIDDLEWARE_SECRET = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

##############
# DEPLOYMENT #
##############
DEPLOYMENT_EXISTING_CHECKOUT = "/Users/rino/dev/djangoplicity/"
DEBUG=True
TEMPLATE_DEBUG=False
DEBUG_SQL=False
DEBUG_PROFILER=False
DEBUG_TOOLBAR = False

#STATIC_ROOT = "%s/static/" % PRJBASE
# MEDIA_ROOT = "/Users/rino/dev/spacetelescope/src/spacetelescope/static/"
MEDIA_ROOT = "/Volumes/ecfwebvol0/diskwa/webdocs/hubble/docs/static/"
# MEDIA_URL = "/static/" #"/static/archives/"
# STATIC_ROOT = "/Users/rino/Workspaces/sites/spacetelescope_media/"
# STATIC_URL = "/static/archives/"

#MEDIA_ROOT = "/tmp/archives/"
#DJANGOPLICITY_MEDIA_ROOT = "/Volumes/webdocs/hubble/docs/static/djangoplicity"

#ARCHIVE_IMPORT_ROOT = "/Volumes/webdocs/hubble/import/"

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
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
CACHES = { 'default': { 'BACKEND': 'django.core.cache.backends.dummy.DummyCache', } }

###########
# LOGGING #
###########
LOGGING_HANDLER = ['console']

##########
# CELERY #
##########
BROKER_URL = 'amqp://spacetelescope:letoveumtold@localhost:5672/spacetelescope_vhost'

CELERY_ALWAYS_EAGER = False

#########
# EMAIL #
#########
#EMAIL_HOST = 'smtphost.hq.eso.org'
#EMAIL_PORT = '25'
