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

#############################
# ENVIRONMENT CONFIGURATION #
#############################
ROOT = "/home/web/hubble"
ROOT_ABS = "/home/web/A/hubblei"
PRJBASE = "%s/projects/spacetelescope.org" % ROOT
DJANGOPLICITY_ROOT = "%s/projects/djangoplicity" % ROOT
LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
ENABLE_SSL = True

#####################
# CONFIG GENERATION #
#####################
WEBSERVERS = (
	('aweb5', '%s1i' % SHORT_NAME, '134.171.74.147' ),
	('aweb6', '%s2i' % SHORT_NAME, '134.171.74.148' ),
	('aweb14', '%s1' % SHORT_NAME, '134.171.75.139' ),
	('aweb15', '%s2' % SHORT_NAME, '134.171.75.140' ),
)
CONFIG_GEN_TEMPLATES_DIR = "%s/conf/templates/" % PRJBASE 
CONFIG_GEN_GENERATED_DIR = "%s/conf/" % PRJBASE

###################
# ERROR REPORTING #
###################
DEBUG = False
SERVE_STATIC_MEDIA = False

##################
# DATABASE SETUP #
##################
DATABASES['default']['USER'] = "spacetelescope"

###############
# MEDIA SETUP #
###############
MEDIA_ROOT = "%s/docs/static" % ROOT
SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"
CSRF_MIDDLEWARE_SECRET = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

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
ARCHIVE_AUTO_RESOURCE_DELETION = True
ARCHIVE_IMPORT_ROOT = "%s/import" % ROOT

#################
# DJANGO ASSETS #
#################
ASSETS_DEBUG = False

########
# SHOP #
########
COPOSWEB_CONFIG_INI = "%s/virtualenv/etc/coposweb.ini" % ROOT
LIVE = False
