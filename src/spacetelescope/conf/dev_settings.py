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
def show_toolbar(request):
	'''
	The default callback checks if the IP is internal, but docker's IP
	addresses are not in INTERNAL_IPS, so we force the display in dev mode
	'''
	return True

DEPLOYMENT_EXISTING_CHECKOUT = "/scratch/scr/hubble/src/"
DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_TOOLBAR = True
DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
	'SHOW_TOOLBAR_CALLBACK': show_toolbar,
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

##################
# DATABASE SETUP #
##################
DATABASES = copy_setting(DATABASES)
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['NAME'] = 'postgres'
DATABASES['default']['HOST'] = 'db'


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
CELERY_BROKER_URL = 'amqp://guest:guest@broker:5672/'

#########
# EMAIL #
#########
#EMAIL_HOST = 'smtphost.hq.eso.org'
#EMAIL_PORT = '25'
