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


#####################
# CONFIG GENERATION #
#####################
WEBSERVERS = (
	('aweb5', '%s1i' % SHORT_NAME, '134.171.74.147' ),
	('aweb6', '%s2i' % SHORT_NAME, '134.171.74.148' ),
	('aweb14', '%s1' % SHORT_NAME, '134.171.75.139' ),
	('aweb15', '%s2' % SHORT_NAME, '134.171.75.140' ),
)
# Needed since config_gen command is usually running on aweb8, and will thus put
# config files in the production environment. 
CONFIG_GEN_TEMPLATES_DIR = "/home/web/A/hubblei/projects/spacetelescope.org/conf/templates/"  
CONFIG_GEN_GENERATED_DIR = "/home/web/A/hubblei/tmp/conf/"

###################
# ERROR REPORTING #
###################
SITE_ENVIRONMENT = 'integration'
DEBUG = True

##################
# DATABASE SETUP #
##################
DATABASES['default']['HOST'] = "mysql1i.hq.eso.org"
DATABASES['default']['PASSWORD'] = "fivjeylvoked"

##########
# CACHE  #
##########
CACHE_BACKEND = "memcached://hubble1i:11211;hubble2i:11211/?timeout=86400"

#########
# EMAIL #
#########
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE-INTEGRATION]'

########	
# AMQP #
########
AMQP_SERVER = "aweb9.hq.eso.org"
CELERY_CACHE_BACKEND = "memcached://aweb9.hq.eso.org:11212/"

########
# SHOP #
########
ORDER_PREFIX = "hbi"