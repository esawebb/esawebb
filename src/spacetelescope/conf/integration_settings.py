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
BUILD_ROOT = "/home/web/%si" % SHORT_NAME

#####################
# CONFIG GENERATION #
#####################

# Needed since config_gen command is usually running on aweb8, and will thus put
# config files in the production environment. 
CONFIG_GEN_TEMPLATES_DIR = "/home/web/A/hubblei/projects/spacetelescope.org/conf/templates/"  
CONFIG_GEN_GENERATED_DIR = "/home/web/A/hubblei/tmp/conf/"

###################
# ERROR REPORTING #
###################
SITE_ENVIRONMENT = 'integration'
DEBUG = False

##############
# DEPLOYMENT #
##############
MANAGEMENT_NODES = ["aweb5"]
BROKERS = ["aweb9"]
WORKERS = ["aweb5","aweb6"]
WORKERS_BEAT_HOST = "aweb5"
WORKERS_CAM_HOST = "aweb6"
WEBSERVER_NODES = ["%s1i" % SHORT_NAME,"%s2i" % SHORT_NAME ]
DEPLOYMENT_TAG = "spacetelescope.org_integration"

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['HOST'] = "mysql1i.hq.eso.org"
DATABASES['default']['PASSWORD'] = "fivjeylvoked"

##########
# CACHE  #
##########
CACHES = {
	'default' : {
		'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
		'KEY_PREFIX' : SHORT_NAME,
		'LOCATION' : [
			'%(short_name)s1i:11211' % { 'short_name' : SHORT_NAME},
			'%(short_name)s2i:11211' % { 'short_name' : SHORT_NAME},
		],
		'TIMEOUT' : 86400
	}
}

#########
# EMAIL #
#########
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE-INTEGRATION]'

###########
# ARCHIVE #
###########
PHOTOSHOP_ROOT = "/home/web/A/importi"

##########	
# CELERY #
##########
BROKER_HOST = "aweb9.hq.eso.org"

########
# SHOP #
########
ORDER_PREFIX = "hbi"