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
ROOT_RELOCATE = "/data/www/hubble"
BUILD_ROOT = "/data/www/%s" % SHORT_NAME
PRJBASE = "%s/src/spacetelescope" % ROOT
DJANGOPLICITY_ROOT = "%s/src/djangoplicity" % ROOT

BUILD_ROOT = ROOT
BUILD_PRJBASE = PRJBASE 
BUILD_DJANGOPLICITY_ROOT = DJANGOPLICITY_ROOT

LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
ENABLE_SSL = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#####################
# CONFIG GENERATION #
#####################
WEBSERVERS = (
	('aweb38', '%s3i' % SHORT_NAME, '134.171.74.208', 'int' ),
	('aweb39', '%s4i' % SHORT_NAME, '134.171.74.209', 'int' ),
	('aweb41', '%s3' % SHORT_NAME, '134.171.75.212', 'prod' ),
	('aweb42', '%s4' % SHORT_NAME, '134.171.75.213', 'prod' ),
)
CONFIG_GEN_TEMPLATES_DIR = "%s/conf/templates/" % PRJBASE 
CONFIG_GEN_GENERATED_DIR = "%s/conf/" % ROOT  # was: "%s/conf/" % TMP_DIR

##############
# DEPLOYMENT #
##############
BUILD_NODES = ["aweb37"]
#WORKER_UID = 2996
#WORKER_GID = 31811
WORKER_LOG_LEVEL = "INFO"
WORKERS_CAM_FREQ = "1.0"

NORMAL_USER = 'epodadm'
SUDO_USER = 'web'

DEPLOYMENT_DEVELOP = False

DEPLOYMENT_PERMS = [
	{'path' : '%(ROOT)s/docs/static/css/', 'user' : None, 'group' : 'epodadm', 'perms' : 'g+ws,o=rx' },
	{'path' : '%(ROOT)s/docs/static/js/', 'user' : None, 'group' : 'epodadm', 'perms' : 'g+ws,o=rx' },
	{'path' : '%(TMP_DIR)s/', 'user' : None, 'group' : 'epodadm', 'perms' : 'g+ws,o=rwx' },
	{'path' : '%(ROOT)s/import', 'user' : None, 'group' : 'epodadm', 'perms' : 'g+ws,o=rx' },
	{'path' : '%(ROOT)s/import/*', 'user' : None, 'group' : 'epodadm', 'perms' : 'g+ws,o=rx' },
	# o+w needded to allow video encoder to write files to the directories.
	{'path' : '%(ROOT)s/import/**/*', 'user' : None, 'group' : '-R epodadm', 'perms' : '-R g+ws,o=rwx' },
	{'path' : '%(ROOT)s/etc/**/*', 'user' : None, 'group' : None, 'perms' : '-R 664' },
]

DEPLOYMENT_SYNC = [
	('%(BUILD_PRJBASE)s/static/','%(BUILD_ROOT)s/docs/static/'),
	('%(BUILD_DJANGOPLICITY_ROOT)s/static/','%(BUILD_ROOT)s/docs/static/djangoplicity/'),
]


###################
# ERROR REPORTING #
###################
DEBUG = False

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['USER'] = "spacetelescope"

###############
# MEDIA SETUP #
###############
SERVE_STATIC_MEDIA = False
MEDIA_ROOT = "%s/docs/static/" % ROOT
STATIC_ROOT = "%s/docs/static/app/" % ROOT
DJANGOPLICITY_MEDIA_ROOT = "%s/static" % DJANGOPLICITY_ROOT
SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"
CSRF_MIDDLEWARE_SECRET = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

############
# SESSIONS #
############
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

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
MP4BOX_PATH = '/usr/bin/MP4Box'

#################
# DJANGO ASSETS #
#################
ASSETS_DEBUG = False

########
# SHOP #
########
COPOSWEB_CONFIG_INI = "%s/virtualenv/etc/coposweb.ini" % ROOT
LIVE = False
