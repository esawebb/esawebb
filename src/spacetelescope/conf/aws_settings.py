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
from djangoplicity.settings import copy_setting

#############################
# ENVIRONMENT CONFIGURATION #
#############################
ROOT = "/home/ubuntu/hubble"
PRJBASE = "%s/projects/spacetelescope.org" % ROOT
DJANGOPLICITY_ROOT = "%s/projects/djangoplicity" % ROOT
LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
ENABLE_SSL = False

#####################
# CONFIG GENERATION #
#####################
WEBSERVERS = (
	('50.17.214.96', '50.17.214.96', '50.17.214.96' ),
	#('aweb6', '%s2i' % SHORT_NAME, '134.171.74.148' ),
	#('aweb14', '%s1' % SHORT_NAME, '134.171.75.139' ),
	#('aweb15', '%s2' % SHORT_NAME, '134.171.75.140' ),
)
CONFIG_GEN_TEMPLATES_DIR = "%s/conf/templates/" % PRJBASE 
CONFIG_GEN_GENERATED_DIR = "%s/conf/" % TMP_DIR

###################
# ERROR REPORTING #
###################
DEBUG = True
SERVE_STATIC_MEDIA = True

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['HOST'] = "localhost"
DATABASES['default']['USER'] = "root"
DATABASES['default']['PASSWORD'] = "WAFTS567"

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
