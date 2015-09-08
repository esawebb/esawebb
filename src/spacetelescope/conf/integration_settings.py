# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from spacetelescope.conf.deployment_settings import *
from djangoplicity.settings import copy_setting

#############################
# ENVIRONMENT CONFIGURATION #
#############################
ROOT_RELOCATE = "/data/www/hubbled"

#############################
# ENVIRONMENT CONFIGURATION #
#############################
BUILD_ROOT = "/data/www/%sd" % SHORT_NAME
BUILDOUT_CONFIG = "conf/integration.cfg"

LOG_DIR = "/data/logs/%sd" % SHORT_NAME

###################
# ERROR REPORTING #
###################
SITE_ENVIRONMENT = 'integration'
DEBUG = False

##############
# DEPLOYMENT #
##############
MANAGEMENT_NODES = ["aweb33"]
BROKERS = ["aweb36"]
WORKERS = ["aweb33", "aweb34"]
WORKERS_BEAT_HOST = "aweb33"
WORKERS_CAM_HOST = "aweb34"
WEBSERVER_NODES = ["%s3i" % SHORT_NAME, "%s4i" % SHORT_NAME ]
DEPLOYMENT_TAG = "spacetelescope.org_int"
DEPLOYMENT_NOTIFICATION = {
	"subject": "[DEPLOY] %(DEPLOYMENT_TAG)s by %(local_user)s",
	"from": "esoepo-monitoring@eso.org",
	"to": ["esoepo-monitoring@eso.org"],
}
PYTHON = "python2.7"

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['HOST'] = "hqdb1i.hq.eso.org"
DATABASES['default']['PASSWORD'] = "fivjeylvoked"
DATABASES['psql']['HOST'] = 'hqdb1i.hq.eso.org'
DATABASES['psql']['PASSWORD'] = 'fivjeylvoked'

##########
# CACHE  #
##########
CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'KEY_PREFIX': SHORT_NAME,
		'LOCATION': [
			'%(short_name)s3i:11211' % { 'short_name': SHORT_NAME},
			'%(short_name)s4i:11211' % { 'short_name': SHORT_NAME},
		],
		'TIMEOUT': 86400
	}
}

#########
# EMAIL #
#########
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE-INTEGRATION]'

##########################
# PHOTOSHOP CELERYWORKER #
##########################
PHOTOSHOP_ROOT = "/home/web/A/importi"
PHOTOSHOP_BROKER['HOST'] = "aweb36.hq.eso.org"

##########
# CELERY #
##########
BROKER_URL = 'amqp://spacetelescope:letoveumtold@aweb36.hq.eso.org:5672/spacetelescope_vhost'

########
# SHOP #
########
ORDER_PREFIX = "hbi"
