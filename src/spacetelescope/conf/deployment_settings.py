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
ROOT = "/home/web/hubble"
PRJBASE = "%s/projects/spacetelescope.org" % ROOT
DJANGOPLICITY_ROOT = "%s/projects/djangoplicity" % ROOT

BUILD_ROOT = ROOT
BUILD_PRJBASE = PRJBASE 
BUILD_DJANGOPLICITY_ROOT = DJANGOPLICITY_ROOT

LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
ENABLE_SSL = True

#####################
# CONFIG GENERATION #
#####################
WEBSERVERS = (
	('aweb5', '%s1i' % SHORT_NAME, '134.171.74.147', 'int' ),
	('aweb6', '%s2i' % SHORT_NAME, '134.171.74.148', 'int' ),
	('aweb14', '%s1' % SHORT_NAME, '134.171.75.139', 'prod' ),
	('aweb15', '%s2' % SHORT_NAME, '134.171.75.140', 'prod' ),
)
CONFIG_GEN_TEMPLATES_DIR = "%s/conf/templates/" % PRJBASE 
CONFIG_GEN_GENERATED_DIR = "%s/conf/" % TMP_DIR

##############
# DEPLOYMENT #
##############
BUILD_NODES = ["aweb8"]
#WORKER_UID = 2996
#WORKER_GID = 31811
WORKER_LOG_LEVEL = "INFO"
WORKERS_CAM_FREQ = "1.0"

NORMAL_USER = 'lchriste'
SUDO_USER = 'web'
APACHE_INIT_MAIN = '/etc/init.d/http.%s.main' % SHORT_NAME
APACHE_INIT_STATIC = '/etc/init.d/http.%s.static' % SHORT_NAME

DEPLOYMENT_DEVELOP = False

DEPLOYMENT_PERMS = [
	{'path' : '%(VIRTUALENV)s/bin/*', 'user' : None, 'group' : None, 'perms' : 'a+x' },
    {'path' : '%(PRJBASE)s/bin/*', 'user' : None, 'group' : None, 'perms' : 'a+x' },
	{'path' : '%(ROOT)s/docs/static/css/', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws,o=rx' },
	{'path' : '%(ROOT)s/docs/static/js/', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws,o=rx' },
	{'path' : '%(LOG_DIR)s/', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws' },
	{'path' : '%(LOG_DIR)s/*', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+w' },
	{'path' : '%(TMP_DIR)s/', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws,o=rwx' },
	{'path' : '%(ROOT)s/import', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws,o=rx' },
	{'path' : '%(ROOT)s/import/*', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws,o=rx' },
	# o+w needded to allow video encoder to write files to the directories.
	{'path' : '%(ROOT)s/import/**/*', 'user' : None, 'group' : '-R w3hst', 'perms' : '-R g+ws,o=rwx' },
]

DEPLOYMENT_SYNC = [
	('%(BUILD_PRJBASE)s/static/','%(BUILD_ROOT)s/docs/static/'),
	('%(BUILD_DJANGOPLICITY_ROOT)s/static/','%(BUILD_ROOT)s/docs/static/djangoplicity/'),
]


###################
# ERROR REPORTING #
###################
DEBUG = False
SERVE_STATIC_MEDIA = False

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['USER'] = "spacetelescope"

###############
# MEDIA SETUP #
###############
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
MP4BOX_PATH = '/usr/local/bin/MP4Box'

#################
# DJANGO ASSETS #
#################
ASSETS_DEBUG = False

########
# SHOP #
########
COPOSWEB_CONFIG_INI = "%s/virtualenv/etc/coposweb.ini" % ROOT
LIVE = False
