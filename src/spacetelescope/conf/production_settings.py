# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from deployment_settings import *
from djangoplicity.settings import copy_setting

###################
# ERROR REPORTING #
###################
SITE_ENVIRONMENT = 'production'

##############
# DEPLOYMENT #
##############
MANAGEMENT_NODES = ["aweb14"]
BROKERS = ["aweb26"]
WORKERS = ["aweb14","aweb15"]
WORKERS_BEAT_HOST = "aweb14"
WORKERS_CAM_HOST = "aweb15"
WEBSERVER_NODES = ["%s1" % SHORT_NAME,"%s2" % SHORT_NAME ]
DEPLOYMENT_TAG = "spacetelescope.org_production"
DEPLOYMENT_REVISION = "spacetelescope.org_integration"
ALLOW_DATABASE_OVERWRITE = False

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['HOST'] = "mysql1.hq.eso.org"
DATABASES['default']['PASSWORD'] = "letoveumtold"

##########
# CACHE  #
##########
CACHES = {
	'default' : {
		'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
		'KEY_PREFIX' : SHORT_NAME,
		'LOCATION' : [
			'%(short_name)s1:11211' % { 'short_name' : SHORT_NAME},
			'%(short_name)s2:11211' % { 'short_name' : SHORT_NAME},
		],
		'TIMEOUT' : 86400
	}
}

#########
# EMAIL #
#########
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE]'

##########	
# CELERY #
##########
BROKER_HOST = "aweb26.hq.eso.org"

########
# SHOP #
########
ORDER_PREFIX = "hb"
LIVE = True