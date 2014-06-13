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

#############################
# ENVIRONMENT CONFIGURATION #
#############################
BUILD_ROOT = "/data/www/%s" % SHORT_NAME

LOG_DIR = "/data/logs/%s" % SHORT_NAME

###################
# ERROR REPORTING #
###################
SITE_ENVIRONMENT = 'production'

##############
# DEPLOYMENT #
##############
BUILDOUT_CONFIG = "conf/production.cfg"
MANAGEMENT_NODES = ["aweb41"]
BROKERS = ["aweb26"]
WORKERS = ["aweb41", "aweb42"]
WORKERS_BEAT_HOST = "aweb41"
WORKERS_CAM_HOST = "aweb42"
WEBSERVER_NODES = ["%s3" % SHORT_NAME, "%s4" % SHORT_NAME ]
DEPLOYMENT_TAG = "spacetelescope.org_prod"
DEPLOYMENT_REVISION = "spacetelescope.org_int"
DEPLOYMENT_NOTIFICATION = {
	"subject" : "[DEPLOY] %(DEPLOYMENT_TAG)s by %(local_user)s",
	"from" : "esoepo-monitoring@eso.org",
	"to" : ["webmaster@eso.org", "esoepo-monitoring@eso.org"],
}
ALLOW_DATABASE_OVERWRITE = False


##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['HOST'] = "hqdb1.hq.eso.org"
DATABASES['default']['PASSWORD'] = "letoveumtold"

##########
# CACHE  #
##########
CACHES = {
	'default' : {
		'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
		'KEY_PREFIX' : SHORT_NAME,
		'LOCATION' : [
			'%(short_name)s3:11211' % { 'short_name' : SHORT_NAME},
			'%(short_name)s4:11211' % { 'short_name' : SHORT_NAME},
		],
		'TIMEOUT' : 86400
	}
}

#########
# EMAIL #
#########
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE]'

##########################	
# PHOTOSHOP CELERYWORKER #
##########################
PHOTOSHOP_ROOT = "/home/web/A/import"
PHOTOSHOP_BROKER['HOST'] = "aweb26.hq.eso.org"

##########	
# CELERY #
##########
BROKER_HOST = "aweb26.hq.eso.org"

########
# SHOP #
########
ORDER_PREFIX = "hb"
COPOSWEB_CONFIG_INI = "%s/etc/coposweb/coposweb-prod.ini" % ROOT
LIVE = True

##########
# SOCIAL #
##########
SOCIAL_FACEBOOK_TOKEN = "144508505618279|5ff52306023505ab445993a2.1-1210975348|12383118425|U_oKxUW-oTKzWHksV5b7I5YCry8"
SOCIAL_TWITTER_TUPLE = ("138725262-pvMvidxE9nB3JYlLkR7aBExaSUkm9TFlzawX8wq7",
						"bClNsjLM33fXqtseS0NeXCMwnsggeS9Gi2z3kGl0c",
						"elGtKvRIq8qVCihslKWRQ",
						"syd83XYDRGEDwr0LaZufxs7t7h766L9UM0foxkH0")
