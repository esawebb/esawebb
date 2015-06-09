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

ROOT_RELOCATE = "/scratch/src/hubble"
ADMINS = (
	('Mathias Andre', 'mandre@eso.org'),
)

#####################
# CONFIG GENERATION #
#####################
SHORT_NAME = 'hubble'
WEBSERVERS = ()
SSL_ASSETS_PREFIX = "www.spacetelescope.org"
CONFIG_GEN_TEMPLATES_DIR = "%s/conf/templates/" % PRJBASE
CONFIG_GEN_GENERATED_DIR = "%s/conf/" % TMP_DIR

SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"
CSRF_MIDDLEWARE_SECRET = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

##############
# DEPLOYMENT #
##############
DEPLOYMENT_EXISTING_CHECKOUT = "/scratch/scr/hubble/src/"
DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_TOOLBAR = True
DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
}
DEBUG_TOOLBAR_PANELS = [
	'debug_toolbar.panels.versions.VersionsPanel',
	'debug_toolbar.panels.timer.TimerPanel',
#	'debug_toolbar.panels.settings.SettingsPanel',
	'debug_toolbar.panels.headers.HeadersPanel',
	'debug_toolbar.panels.request.RequestPanel',
	'debug_toolbar.panels.sql.SQLPanel',
#	'debug_toolbar.panels.staticfiles.StaticFilesPanel',
	'debug_toolbar.panels.templates.TemplatesPanel',
	'debug_toolbar.panels.cache.CachePanel',
	'debug_toolbar.panels.signals.SignalsPanel',
	'debug_toolbar.panels.logging.LoggingPanel',
	'debug_toolbar.panels.redirects.RedirectsPanel',
]

MEDIA_ROOT = "/media/ecfwebstore/ecfwebvol0/diskwa/webdocs/hubble/docs/static/"
#MEDIA_ROOT = "/tmp/archives/"
#DJANGOPLICITY_MEDIA_ROOT = "/Volumes/webdocs/hubble/docs/static/djangoplicity"

#ARCHIVE_IMPORT_ROOT = "/Volumes/webdocs/hubble/import/"

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
#DATABASES['default']['HOST'] = "mysql1i.hq.eso.org"
#DATABASES['default']['PASSWORD'] = "fivjeylvoked"

#DATABASES['default']['USER'] = "spacetelescope"
#DATABASES['default']['HOST'] = "mysql1.hq.eso.org"
#DATABASES['default']['PASSWORD'] = "letoveumtold"

###############
# MEDIA SETUP #
###############
#MEDIA_ROOT = "/Volumes/webdocs/hubble/docs/static"

##########
# CACHE  #
##########
CACHES = {
	'notdefault' : {
		'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
		'KEY_PREFIX' : 'eso',
		'LOCATION' : [
			'127.0.0.1:11211',
		],
		'TIMEOUT' : 86400
	},
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	}
}

###########
# LOGGING #
###########
LOGGING_HANDLER = ['console']

##########
# CELERY #
##########
BROKER_URL = 'amqp://spacetelescope:letoveumtold@localhost:5672/spacetelescope_vhost'

CELERY_ALWAYS_EAGER = False

#########
# EMAIL #
#########
#EMAIL_HOST = 'smtphost.hq.eso.org'
#EMAIL_PORT = '25'
