# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
import copy
from default_settings import *

#############################
# ENVIRONMENT CONFIGURATION #
#############################
ROOT = "/home/web/hubblei/"
PRJBASE = "%s/projects/spacetelescope.org" % ROOT
DJANGOPLICITY_ROOT = "%s/projects/djangoplicity" % ROOT
LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
ENABLE_SSL = True

###################
# ERROR REPORTING #
###################
DEBUG = False
SERVE_STATIC_MEDIA = False

##################
# DATABASE SETUP #
##################
DATABASES = copy.deepcopy(DATABASES)
DATABASES['default']['USER'] = "spacetelescope"
DATABASES['default']['HOST'] = "mysql1i.hq.eso.org"
DATABASES['default']['PASSWORD'] = "fivjeylvoked"

###############
# MEDIA SETUP #
###############
MEDIA_ROOT = "%s/docs/static" % ROOT
SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"
CSRF_MIDDLEWARE_SECRET = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

##########
# CACHE  #
##########
CACHE_BACKEND = "memcached://hubble1i:11211;hubble2i:11211/?timeout=86400"

################
# FILE UPLOADS #
################
FILE_UPLOAD_TEMP_DIR = TMP_DIR

#########
# EMAIL #
#########
EMAIL_HOST = 'smtphost.hq.eso.org'
EMAIL_PORT = '25'

#########
# GEOIP #
#########
GEOIP_PATH = "%s/virtualenv/share/GeoIP" % ROOT
GEOIP_LIBRARY_PATH = "%s/virtualenv/lib/libGeoIP.dylib" % ROOT

###########
# ARCHIVE #
###########
ARCHIVE_AUTO_RESOURCE_DELETION = False
ARCHIVE_IMPORT_ROOT = "%s/import" % ROOT

########
# SHOP #
########
COPOSWEB_CONFIG_INI = "%s/virtualenv/etc/coposweb.ini" % ROOT
LIVE = False
