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

#############################
# ENVIRONMENT CONFIGURATION #
#############################
ROOT = "/Users/%s/Workspaces/sites/spacetelescope" % getpass.getuser()
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
        'OPTIONS' : {},
        'TEST_CHARSET' : 'utf8',
        'TEST_COLLATION' : 'utf8_general_ci',
        'TEST_MIRROR' : None,
        'TEST_NAME' : None, # "test_" + DATABASE_NAME
    }
}

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
ARCHIVE_IMPORT_ROOT = "/Volumes/webdocs/importi"

########	
# AMQP #
########
AMQP_SERVER = "aweb9.hq.eso.org"
AMQP_PORT = 5672
AMQP_USER = "taskexchange"
AMQP_PASSWORD = "D1~odvcO7"
AMQP_VHOST = "taskexchange"

CELERY_BACKEND = "cache"
CELERY_CACHE_BACKEND = "memcached://aweb9.hq.eso.org:11212/"
CELERY_AMQP_EXCHANGE = "tasks"
CELERY_AMQP_PUBLISHER_ROUTING_KEY = "task.regular"
CELERY_AMQP_CONSUMER_QUEUE = "regular_tasks"
CELERY_AMQP_CONSUMER_ROUTING_KEY = "task.#"
CELERY_AMQP_EXCHANGE_TYPE = "topic"

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