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

SITE_ENVIRONMENT = 'integration'

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