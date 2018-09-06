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

#####################
# CONFIG GENERATION #
#####################
SHORT_NAME = 'hubble'
WEBSERVERS = ()
SSL_ASSETS_PREFIX = "www.spacetelescope.org"

SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

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

MEDIA_ROOT = "/media/epodweb/hubble/docs/static/"
#MEDIA_ROOT = "/tmp/"
#DJANGOPLICITY_MEDIA_ROOT = "/Volumes/webdocs/hubble/docs/static/djangoplicity"

#ARCHIVE_IMPORT_ROOT = "/Volumes/webdocs/hubble/import/"

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['USER'] = "mandre"
DATABASES['default']['PASSWORD'] = "Hirshaj3"

###############
# MEDIA SETUP #
###############
#MEDIA_ROOT = "/Volumes/webdocs/hubble/docs/static"

##########
# CACHE  #
##########
CACHES = {
	'notdefault': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'KEY_PREFIX': 'eso',
		'LOCATION': [
			'127.0.0.1:11211',
		],
		'TIMEOUT': 86400
	},
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	}
}

##########
# CELERY #
##########
CELERY_BROKER_URL = 'amqp://spacetelescope:letoveumtold@localhost:5672/spacetelescope_vhost'

CELERY_TASK_ALWAYS_EAGER = False

#########
# EMAIL #
#########
#EMAIL_HOST = 'smtphost.hq.eso.org'
#EMAIL_PORT = '25'
