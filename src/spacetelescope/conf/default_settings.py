# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

import getpass
import sys

#############################
# ENVIRONMENT CONFIGURATION #
#############################
ROOT = "/Users/%s/Workspaces/sites/spacetelescope" % getpass.getuser()
BUILD_ROOT = ROOT
PRJBASE = "%s/projects/spacetelescope.org" % ROOT
DJANGOPLICITY_ROOT = "%s/projects/djangoplicity" % ROOT
LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
ENABLE_SSL = False

#####################
# CONFIG GENERATION #
#####################
SHORT_NAME = 'hubble'
WEBSERVERS = ()
SSL_ASSETS_PREFIX = "www.spacetelescope.org"
CONFIG_GEN_TEMPLATES_DIR = "%s/conf/templates/" % PRJBASE 
CONFIG_GEN_GENERATED_DIR = "%s/conf/" % TMP_DIR

##############
# DEPLOYMENT #
##############
BUILD_NODES = ["localhost"]
MANAGEMENT_NODES = ["localhost"]
BROKERS = ["localhost"]

WORKERS = ["localhost"]
WORKERS_BEAT_HOST = "localhost"
WORKERS_CAM_HOST = "localhost"
WORKER_UID = None
WORKER_GID = None
WORKER_LOG_LEVEL = "INFO"
WORKERS_CAM_FREQ = "1.0"

NORMAL_USER = None
SUDO_USER = None

APACHE_INIT_MAIN = '/etc/init.d/apache2'
APACHE_INIT_STATIC = '/etc/init.d/apache2'
DEPLOYMENT_TAG = None
DEPLOYMENT_REVISION = None
DEPLOYMENT_DEVELOP = True
DEPLOYMENT_EXISTING_CHECKOUT = None
ALLOW_DATABASE_OVERWRITE = True

###################
# ERROR REPORTING #
###################
SITE_ENVIRONMENT = 'local'
DEBUG = True
DEBUG_SQL = False
DEBUG_PROFILER = False
DEBUG_TOOLBAR = False
TEMPLATE_DEBUG = False
SEND_BROKEN_LINK_EMAILS = False

ADMINS = (
	('EPO Monitoring','esoepo-monitoring@eso.org'),
)

LOGGING_HANDLER = ['file']

##################
# DATABASE SETUP #
##################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spacetelescope',
        'USER' : 'root',
        'PASSWORD' : '',
        'HOST' : 'localhost',
        'PORT' : '3306',
        'OPTIONS' : {
			'connect_timeout' : 15,
		},
        'TEST_CHARSET' : 'utf8',
        'TEST_COLLATION' : 'utf8_general_ci',
        'TEST_MIRROR' : None,
        'TEST_NAME' : None, # "test_" + DATABASE_NAME
    }
}

if 'test' in sys.argv:
	DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
	
###############
# MEDIA SETUP #
###############
SERVE_STATIC_MEDIA = True
MEDIA_ROOT = "%s/static" % PRJBASE
MEDIA_URL = "/static/"
DJANGOPLICITY_MEDIA_URL = "/static/djangoplicity/"
DJANGOPLICITY_MEDIA_ROOT = "%s/static" % DJANGOPLICITY_ROOT
ADMIN_MEDIA_PREFIX = "/static/media/"


# Make this unique, and don't share it with anybody.
SECRET_KEY = "sadfpn870742kfasbvancp837rcnp3w8orypbw83ycnspo8r7"
CSRF_MIDDLEWARE_SECRET = "sadfpn870742kfasbvancp837rcnp3w8orypbw83ycnspo8r7"

##########
# CACHE  #
##########
CACHES = {
	'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': SHORT_NAME,
    }
}

###############################
# MIDDLEWARE AND APPLICATIONS #
###############################
ENABLE_REDIRECT_MIDDLEWARE = False
REDIRECT_MIDDLEWARE_URI = 'http://www.spacetelescope.org'	

############
# SESSIONS #
############
SESSION_ENGINE='django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE=86400
SESSION_COOKIE_DOMAIN=None

################
# FILE UPLOADS #
################
FILE_UPLOAD_TEMP_DIR = TMP_DIR
FILE_UPLOAD_PERMISSIONS = 0666

#########
# EMAIL #
#########
SERVER_EMAIL = 'nobody@eso.org'
DEFAULT_FROM_EMAIL = 'nobody@eso.org'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE-LOCAL]'

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
PHOTOSHOP_ROOT = "/Users/%s/Workspaces/sites/import" % getpass.getuser()

##########	
# CELERY #
##########
BROKER_HOST = "localhost"
BROKER_USER = "spacetelescope"
BROKER_PASSWORD = "letoveumtold"
BROKER_VHOST = "spacetelescope_vhost"
BROKER_USE_SSL = False

CELERY_ALWAYS_EAGER=False

#################
# DJANGO ASSETS #
#################
ASSETS_DEBUG = True

########
# SHOP #
########
COPOSWEB_CONFIG_INI = "%s/conf/coposweb.ini" % PRJBASE
LIVE = False
ORDER_PREFIX = "hbl"

##########
# SOCIAL #
##########
SOCIAL_FACEBOOK_TOKEN = "187807957898842|a7f1fed4a89e26492133c6e4-100001473653251|141347899254844|K4lqzDRBPyAVFa7msmusumliPwI"
SOCIAL_TWITTER_TUPLE = ("226991078-bHYf0sHAUEs1v6fjnxy8F0KjTLtSLnqTpyKx2Bqh",
		                "oiRDpzBIZUmQ1m8xxrw16aiYBAMjBx9vEi4ddgLOjzc",
		                "uS6hO2sV6tDKIOeVjhnFnQ",
		                "MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk")