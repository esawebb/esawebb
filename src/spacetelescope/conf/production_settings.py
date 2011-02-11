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

SITE_ENVIRONMENT = 'production'

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['HOST'] = "mysql1.hq.eso.org"
DATABASES['default']['PASSWORD'] = "letoveumtold"

##########
# CACHE  #
##########
CACHE_BACKEND = "memcached://%(short_name)s1:11211;%(short_name)s2:11211/?timeout=86400" % { 'short_name' : SHORT_NAME}

#########
# EMAIL #
#########
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE]'

########	
# AMQP #
########
AMQP_SERVER = "taskexchange.hq.eso.org"
CELERY_CACHE_BACKEND = "memcached://taskexchange.hq.eso.org:11212/"

########
# SHOP #
########
ORDER_PREFIX = "hb"