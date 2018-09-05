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

#############################
# ENVIRONMENT CONFIGURATION #
#############################
ROOT = '/app'
PRJBASE = "%s/src/spacetelescope" % ROOT
DJANGOPLICITY_ROOT = "%s/src/djangoplicity" % ROOT

BUILD_ROOT = ROOT
BUILD_PRJBASE = PRJBASE
BUILD_DJANGOPLICITY_ROOT = DJANGOPLICITY_ROOT
BUILDOUT_CONFIG = "buildout.cfg"

LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
ENABLE_SSL = False
ALLOW_SSL = True
SECURE_PROXY_SSL_HEADER = None
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

#####################
# CONFIG GENERATION #
#####################
SHORT_NAME = 'hubble'
WEBSERVERS = ()
SSL_ASSETS_PREFIX = "www.spacetelescope.org"

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
WORKERS_QUEUE = "celery"

NORMAL_USER = None
SUDO_USER = None

NGINX_INIT = '/etc/init.d/nginx'
DEPLOYMENT_TAG = None
DEPLOYMENT_REVISION = None
DEPLOYMENT_DEVELOP = True
DEPLOYMENT_EXISTING_CHECKOUT = None
DEPLOYMENT_NOTIFICATION = None
ALLOW_DATABASE_OVERWRITE = True

SUPERVISORTCTL_PROCESS = 'gunicorn-' + SHORT_NAME

###################
# ERROR REPORTING #
###################
SITE_ENVIRONMENT = 'local'
DEBUG = True
DEBUG_TOOLBAR = False
TEMPLATE_DEBUG = False
SEND_BROKEN_LINK_EMAILS = False

ADMINS = (
	('EPO Monitoring', 'esoepo-monitoring@eso.org'),
)

LOGGING_HANDLER = ['file', 'mail_admins']

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


###############
# MEDIA SETUP #
###############
SERVE_STATIC_MEDIA = True
MEDIA_ROOT = "%s/static/" % PRJBASE
MEDIA_URL = "/static/"
STATIC_ROOT = "%s/static/app/" % PRJBASE
STATIC_URL = "/static/app/"
DJANGOPLICITY_MEDIA_URL = "/static/app/djangoplicity/"
DJANGOPLICITY_MEDIA_ROOT = "%s/static" % DJANGOPLICITY_ROOT
ADMIN_MEDIA_PREFIX = "/static/app/admin/"

MIDENTIFY_PATH = '/usr/bin/midentify'

DEBUG_TOOLBAR_PANELS = [
#	'debug_toolbar.panels.versions.VersionsPanel',
#	'debug_toolbar.panels.timer.TimerPanel',
#	'debug_toolbar.panels.settings.SettingsPanel',
#	'debug_toolbar.panels.headers.HeadersPanel',
#	'debug_toolbar.panels.request.RequestPanel',
#	'debug_toolbar.panels.sql.SQLPanel',
#	'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#	'debug_toolbar.panels.templates.TemplatesPanel',
#	'debug_toolbar.panels.cache.CachePanel',
#	'debug_toolbar.panels.signals.SignalsPanel',
#	'debug_toolbar.panels.logging.LoggingPanel',
#	'debug_toolbar.panels.redirects.RedirectsPanel',
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "sadfpn870742kfasbvancp837rcnp3w8orypbw83ycnspo8r7"

##########
# CACHE  #
##########
CACHES = {
	'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': SHORT_NAME,
    }
}

############
# SESSIONS #
############
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400
SESSION_COOKIE_DOMAIN = None

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
MP4BOX_PATH = '/Applications/Osmo4.app/Contents/MacOS/MP4Box'
MP4FRAGMENT_PATH = '/usr/bin/mp4fragment'

##########
# CELERY #
##########
CELERY_BROKER_USE_SSL = False
CELERY_BROKER_URL = 'amqp://spacetelescope:letoveumtold@localhost:5672/spacetelescope_vhost'

CELERY_TASK_ALWAYS_EAGER = False

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

########
# LDAP #
########
DISABLE_LDAP = False

##########
# SOCIAL #
##########
SOCIAL_FACEBOOK_TOKEN = "187807957898842|a7f1fed4a89e26492133c6e4-100001473653251|141347899254844|K4lqzDRBPyAVFa7msmusumliPwI"
SOCIAL_TWITTER_TUPLE = ("226991078-bHYf0sHAUEs1v6fjnxy8F0KjTLtSLnqTpyKx2Bqh",
		                "oiRDpzBIZUmQ1m8xxrw16aiYBAMjBx9vEi4ddgLOjzc",
		                "uS6hO2sV6tDKIOeVjhnFnQ",
		                "MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk")
