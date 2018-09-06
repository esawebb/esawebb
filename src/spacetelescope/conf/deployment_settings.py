# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from spacetelescope.conf.default_settings import *
from djangoplicity.settings import copy_setting

#############################
# ENVIRONMENT CONFIGURATION #
#############################
PRJBASE = "%s/src/spacetelescope" % ROOT
DJANGOPLICITY_ROOT = "%s/src/djangoplicity" % ROOT

ENABLE_SSL = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING_HANDLER = ['file']

#####################
# CONFIG GENERATION #
#####################
WEBSERVERS = (
	('aweb33', '%s3i' % SHORT_NAME, '134.171.74.208', 'int' ),
	('aweb34', '%s4i' % SHORT_NAME, '134.171.74.209', 'int' ),
	('aweb41', '%s3' % SHORT_NAME, '134.171.75.212', 'prod' ),
	('aweb42', '%s4' % SHORT_NAME, '134.171.75.213', 'prod' ),
)

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
	{'path': '%(ROOT)s/docs/static/css/', 'user': None, 'group': 'epodadm', 'perms': 'g+ws,o=rx' },
	{'path': '%(ROOT)s/docs/static/js/', 'user': None, 'group': 'epodadm', 'perms': 'g+ws,o=rx' },
	{'path': '%(TMP_DIR)s/', 'user': None, 'group': 'epodadm', 'perms': 'g+ws,o=rwx' },
	{'path': '%(ROOT)s/import', 'user': None, 'group': 'epodadm', 'perms': 'g+ws,o=rx' },
	{'path': '%(ROOT)s/import/*', 'user': None, 'group': 'epodadm', 'perms': 'g+ws,o=rx' },
	# o+w needded to allow video encoder to write files to the directories.
	{'path': '%(ROOT)s/import/**/*', 'user': None, 'group': '-R epodadm', 'perms': '-R g+ws,o=rwx' },
	{'path': '%(ROOT)s/etc/**/*', 'user': None, 'group': None, 'perms': '-R 664' },
]

DEPLOYMENT_SYNC = [
	('%(BUILD_PRJBASE)s/static/', '%(BUILD_ROOT)s/docs/static/'),
	('%(BUILD_DJANGOPLICITY_ROOT)s/static/', '%(BUILD_ROOT)s/docs/static/djangoplicity/'),
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
DATABASES['default']['CONN_MAX_AGE'] = 600

###############
# MEDIA SETUP #
###############
SERVE_STATIC_MEDIA = False
MEDIA_ROOT = "%s/docs/static/" % ROOT
STATIC_ROOT = "%s/docs/static/app/" % ROOT
DJANGOPLICITY_MEDIA_ROOT = "%s/static" % DJANGOPLICITY_ROOT
SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

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
MP4FRAGMENT_PATH = '/opt/bento4/bin/mp4fragment'

#################
# DJANGO ASSETS #
#################
ASSETS_DEBUG = False

########
# SHOP #
########
COPOSWEB_CONFIG_INI = "%s/virtualenv/etc/coposweb.ini" % ROOT
LIVE = False
