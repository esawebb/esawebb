# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

import sys


##################
# DATABASE SETUP #
##################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spacetelescope',
        'USER': 'spacetelescope',
        'PASSWORD': '',
        'HOST': 'localhost',
        'CONN_MAX_AGE': 0,
    }
}

if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


##########
# CACHE  #
##########

############
# SESSIONS #
############

################
# FILE UPLOADS #
################

#########
# EMAIL #
#########

#########
# GEOIP #
#########

###########
# ARCHIVE #
###########

##########
# CELERY #
##########

#################
# DJANGO ASSETS #
#################

########
# SHOP #
########
LIVE = False

########
# LDAP #
########
DISABLE_LDAP = False

##########
# SOCIAL #
##########
