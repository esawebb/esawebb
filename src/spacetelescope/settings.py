# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from djangoplicity.settings import import_settings		
import os
import re

local_settings = import_settings('spacetelescope')
LOCAL_SETTINGS_MODULE = local_settings.LOCAL_SETTINGS_MODULE

#############################
# ENVIRONMENT CONFIGURATION #
#############################
ROOT = local_settings.ROOT
PRJBASE = local_settings.PRJBASE
PRJNAME = 'spacetelescope.org'
DJANGOPLICITY_ROOT = local_settings.DJANGOPLICITY_ROOT
LOG_DIR = local_settings.LOG_DIR
TMP_DIR = local_settings.TMP_DIR
ENABLE_SSL = local_settings.ENABLE_SSL
GA_ID = "UA-2368492-6"

#####################
# CONFIG GENERATION #
#####################
SHORT_NAME = local_settings.SHORT_NAME
WEBSERVERS = local_settings.WEBSERVERS
SSL_ASSETS_PREFIX = local_settings.SSL_ASSETS_PREFIX
CONFIG_GEN_TEMPLATES_DIR = local_settings.CONFIG_GEN_TEMPLATES_DIR 
CONFIG_GEN_GENERATED_DIR = local_settings.CONFIG_GEN_GENERATED_DIR

###################
# ERROR REPORTING #
###################
INTERNAL_IPS = ('127.0.0.1',)

SITE_ENVIRONMENT = local_settings.SITE_ENVIRONMENT
DEBUG = local_settings.DEBUG
DEBUG_SQL = local_settings.DEBUG_SQL
DEBUG_PROFILER = local_settings.DEBUG_PROFILER
DEBUG_TOOLBAR = local_settings.DEBUG_TOOLBAR
TEMPLATE_DEBUG = local_settings.TEMPLATE_DEBUG
SEND_BROKEN_LINK_EMAILS = local_settings.SEND_BROKEN_LINK_EMAILS

ADMINS = local_settings.ADMINS
MANAGERS = ADMINS

SERVE_STATIC_MEDIA = local_settings.SERVE_STATIC_MEDIA

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    #'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    #'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

##################
# DATABASE SETUP #
##################
DATABASES = local_settings.DATABASES

FIXTURE_DIRS = (
	PRJBASE + '/fixtures',
	DJANGOPLICITY_ROOT + '/fixtures',
)

########################
# INTERNATIONALIZAION  #
########################
# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
gettext_noop = lambda s: s
_ = gettext_noop 

LANGUAGES = (
	( 'en', gettext_noop( 'English' ) ),
)

LANGUAGE_CODE = 'en'

FORMAT_MODULE_PATH = 'spacetelescope.formats'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
USE_L10N = True

#LOCALE_PATHS = ( DJANGOPLICITY_ROOT + "/locale", PRJBASE + "/locale", )

# Default date and time formats (con be overridden by locale)
DATE_FORMAT = gettext_noop('j F Y')
DATE_LONG_FORMAT = gettext_noop('j F Y')
DATETIME_FORMAT = gettext_noop('M j, Y, H:i T')
DATETIME_LONG_FORMAT = gettext_noop('M j, Y y, H:i T')
MONTH_DAY_FORMAT = gettext_noop('F j')
TIME_FORMAT = gettext_noop('H:i T')
YEAR_MONTH_FORMAT = gettext_noop('F Y')
WIDGET_FORMAT = gettext_noop("j/m/Y")

###############
# MEDIA SETUP #
###############
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = local_settings.MEDIA_ROOT


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = local_settings.MEDIA_URL


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = local_settings.ADMIN_MEDIA_PREFIX
DJANGOPLICITY_MEDIA_URL = local_settings.DJANGOPLICITY_MEDIA_URL
DJANGOPLICITY_MEDIA_ROOT = local_settings.DJANGOPLICITY_MEDIA_ROOT

# Staticfiles app
STATICFILES_DIRS = [
	( 'djangoplicity', DJANGOPLICITY_MEDIA_ROOT ),
]

STATIC_ROOT = local_settings.STATIC_ROOT
STATIC_URL = local_settings.STATIC_URL

# Make this unique, and don't share it with anybody.
SECRET_KEY = local_settings.SECRET_KEY
CSRF_MIDDLEWARE_SECRET = local_settings.CSRF_MIDDLEWARE_SECRET

##########
# CACHE  #
##########
CACHES = local_settings.CACHES
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = SHORT_NAME
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

### keyedcached settings:
CACHE_TIMEOUT = CACHE_MIDDLEWARE_SECONDS 
CACHE_PREFIX = SHORT_NAME

USE_ETAGS = True

#############
# TEMPLATES #
#############
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.request',
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
    'django.core.context_processors.static',
	'djangoplicity.utils.context_processors.site_environment',
	'djangoplicity.utils.context_processors.project_environment',
	'djangoplicity.utils.context_processors.google_analytics_id',
	'djangoplicity.utils.context_processors.djangoplicity_environment',
)

ROOT_URLCONF = 'spacetelescope.urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	PRJBASE + '/templates',
	DJANGOPLICITY_ROOT + '/templates',
)

###############################
# MIDDLEWARE AND APPLICATIONS #
###############################
MIDDLEWARE_CLASSES = (
	# Middleware hack to do some initialization when django is started. Middleware is removed immediately afterwards.
	'djangoplicity.startup.StartupMiddleware',
					
	# Compresses content for browsers that understand gzip compression (all modern browsers).
	'django.middleware.gzip.GZipMiddleware', # Response

	# Handles conditional GET operations. If the response has a ETag or Last-Modified header, 
	# and the request has If-None-Match or If-Modified-Since, the response is replaced by an 
	# HttpNotModified.
	'django.middleware.http.ConditionalGetMiddleware',
	
	# The CsrfMiddleware class provides easy-to-use protection against Cross Site Request Forgeries.
	#'django.contrib.csrf.middleware.CsrfMiddleware',
	
	# Based on 'SSL' and 'SSLAllow' boolean URL paramters it will redirect to
	# HTTP or HTTPS.
	'sslmiddleware.SSLRedirect',
)

if DEBUG:
	# Add label to all HTML pages displaying the environment
	MIDDLEWARE_CLASSES += ('djangoplicity.utils.middleware.SiteEnvironmentMiddleware',)

if DEBUG_SQL:
	# Show all SQL queries being executed as well execution time.
	MIDDLEWARE_CLASSES += ('djangoplicity_ext.middleware.sqlmiddleware.SQLLogMiddleware',)

if DEBUG_PROFILER:
	# Enabled profiling of code. Add ?prof to URL to profile request.
	MIDDLEWARE_CLASSES += ('djangoplicity_ext.middleware.profilemiddleware.ProfileMiddleware',)
	
if DEBUG_TOOLBAR:
	# Add debug toolbar to request
	MIDDLEWARE_CLASSES += (
		'debug_toolbar.middleware.DebugToolbarMiddleware',
	)
	
ENABLE_REDIRECT_MIDDLEWARE = local_settings.ENABLE_REDIRECT_MIDDLEWARE
REDIRECT_MIDDLEWARE_URI = local_settings.REDIRECT_MIDDLEWARE_URI	
	

MIDDLEWARE_CLASSES += (
	# Enables session support
	'django.contrib.sessions.middleware.SessionMiddleware', # Request/Response (db)
	
    # Adds the user attribute, representing the currently-logged-in user, to every incoming 
    # HttpRequest object. 
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Request
)    

if USE_I18N:
	MIDDLEWARE_CLASSES += (
    	# Sets local for request based on URL prefix.
	    'djangoplicity.translation.middleware.LocaleMiddleware', # Request/Response
    )

MIDDLEWARE_CLASSES += (    
    # - Forbids access to user agents in the DISALLOWED_USER_AGENTS setting
    # - Performs URL rewriting based on the APPEND_SLASH and PREPEND_WWW settings.
    # - Handles ETags based on the USE_ETAGS setting.
    'django.middleware.common.CommonMiddleware', # Request/Response
    
)


MIDDLEWARE_CLASSES += (
	# Module for URL redirection. 
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware', # Response
	
	# Module for URL redirection based on regular expressions
	'djangoplicity.utils.middleware.RegexRedirectMiddleware', # Response
	
	# Djangoplicity static pages
	'djangoplicity.pages.middleware.PageFallbackMiddleware', # Response
)

if ENABLE_REDIRECT_MIDDLEWARE:
	MIDDLEWARE_CLASSES += (
		'djangoplicity.contrib.redirects.middleware.SinkRedirectMiddleware',
		)
		
INSTALLED_APPS = ()

if USE_I18N:
	INSTALLED_APPS += (
		'djangoplicity.translation',
		'rosetta',
	)

INSTALLED_APPS += (
	'django.contrib.staticfiles',
	'django.contrib.sites',
	'satchmo_store.shop',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
	'django.contrib.humanize',
	'django.contrib.sitemaps',
	'djangoplicity.menus',
	'djangoplicity.pages',
	'djangoplicity.cron',
	'djangoplicity.media',
	'djangoplicity.jobs',
	'django.contrib.redirects',
	'djangoplicity.archives',
	'djangoplicity.archives.contrib.satchmo.freeorder',
    'djangoplicity.archives.contrib.security',
	'djangoplicity.archives.contrib.inventory_control',
	'djangoplicity.announcements',
	'djangoplicity.releases',
	'djangoplicity.products',  
	'djangoplicity.search',
	'djangoplicity.metadata',  
	'djangoplicity.authtkt',
	'djangoplicity.google',
	'djangoplicity.cache',
	'djangoplicity.inventory',
	'djangoplicity.adminhistory',
    'djangoplicity.utils',
    'djangoplicity.celery',
    #'djangoplicity.events',
    'djangoplicity.mailinglists',
    'djangoplicity.newsletters',
    'djangoplicity.iframe',
    #'djangoplicity.contacts',
    #'djangoplicity.customsearch',
    'djangoplicity.admincomments',
    'djangoplicity.simplearchives',
    #'djangoplicity.eventcalendar',
    'djangoplicity.actions',
	'spacetelescope',
	'djcelery',
	'mptt',
	'django_extensions',
	'django_assets',
	# Satchmo
	#'registration',
	'sorl.thumbnail',
	'keyedcache',
	'livesettings',
	'satchmo_utils',
	'satchmo_store.contact',
	'product',
	'shipping',
	'payment',
	'djangoplicity.coposweb',
    'l10n',
    'tax',
    'tax.modules.no',
    'app_plugins',
    'shipping.modules.tieredweight',
    'django_config_gen',
    'tinymce',
)


if DEBUG_TOOLBAR:
	INSTALLED_APPS += (
		'debug_toolbar',
	)

INSTALLED_APPS += (
	'south',
)

############
# SESSIONS #
############
SESSION_ENGINE=local_settings.SESSION_ENGINE
SESSION_COOKIE_AGE=local_settings.SESSION_COOKIE_AGE
SESSION_COOKIE_DOMAIN=local_settings.SESSION_COOKIE_DOMAIN

################
# FILE UPLOADS #
################
FILE_UPLOAD_TEMP_DIR = local_settings.FILE_UPLOAD_TEMP_DIR
FILE_UPLOAD_PERMISSIONS = 0666
#FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 <-- default 

#########
# EMAIL #
#########
SERVER_EMAIL = local_settings.SERVER_EMAIL
DEFAULT_FROM_EMAIL = local_settings.DEFAULT_FROM_EMAIL
EMAIL_HOST = local_settings.EMAIL_HOST
EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
EMAIL_PORT = local_settings.EMAIL_PORT
EMAIL_USE_TLS = local_settings.EMAIL_USE_TLS
EMAIL_SUBJECT_PREFIX = local_settings.EMAIL_SUBJECT_PREFIX

##################
# AUTHENTICATION #
##################
AUTHENTICATION_BACKENDS = ( 
	'django_auth_ldap.backend.LDAPBackend',
	'django.contrib.auth.backends.ModelBackend',
)
#AUTH_PROFILE_MODULE = ''
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

#############
# LDAP AUTH #
#############
import ldap
from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType

AUTH_LDAP_SERVER_URI = "ldaps://ldap.ads.eso.org:636/ads.eso.org"

AUTH_LDAP_GLOBAL_OPTIONS = {
	ldap.OPT_REFERRALS : 0,
	ldap.OPT_PROTOCOL_VERSION : 3,
	ldap.OPT_X_TLS_REQUIRE_CERT : ldap.OPT_X_TLS_NEVER
}

AUTH_LDAP_BIND_DN = "xskioskldap"
AUTH_LDAP_BIND_PASSWORD = "LDAP1420"
AUTH_LDAP_USER_SEARCH = LDAPSearch( "DC=ads,DC=eso,DC=org",
    ldap.SCOPE_SUBTREE, "(&(objectCategory=user)(objectClass=person)(sAMAccountName=%(user)s)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))" )

AUTH_LDAP_USER_ATTR_MAP = {
          "first_name": "givenName",
          "last_name": "sn",
          "email": "mail"
}

AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()
AUTH_LDAP_GROUP_SEARCH = LDAPSearch( "dc=ads,dc=eso,dc=org",
    ldap.SCOPE_SUBTREE, "(objectClass=group)"
)

# Defaults:
# - ePOD staff will get active/staff account - but no permissions.
# - All ESO staff will get an inactive account on login - this account has to manually be activated.
AUTH_LDAP_ALWAYS_UPDATE_USER = False # Prevent user from being updated every time a user logs in.

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
	"is_active": "CN=SA-PAD-EPR,OU=Garching,OU=Shared Acess Groups,OU=Groups,DC=ads,DC=eso,DC=org",
	"is_staff": "CN=SA-PAD-EPR,OU=Garching,OU=Shared Acess Groups,OU=Groups,DC=ads,DC=eso,DC=org",
}

############
# AUTH_TKT #
############
AUTH_TKT_UNAUTH_URL = '/access_denied/'
AUTH_TKT_COOKIE_NAME = 'auth_tkt'
AUTH_TKT_HTACCESS = '.esoacc'
# AUTH_TKT_REDIRECT_FIELD_NAME = 'next'
# AUTH_TKT_IGNOREIP = 'off'
# AUTH_TKT_TIMEOUT_URL = ''
# AUTH_TKT_FILEPERMS = 


#########
# GEOIP #
#########
GEOIP_PATH =local_settings.GEOIP_PATH
GEOIP_LIBRARY_PATH = local_settings.GEOIP_LIBRARY_PATH

#########
# PAGES #
#########
PAGE_TEMPLATE_CHOICES = (
    ('pages/page_onecolumn.html','Default one column layout'),
    ('pages/page_twocolumn.html','Default two column layout'),
    ('pages/page_search.html','Google custom search layout')
)

#############
# PAGIANTOR #
#############
DEFAULT_PAGINATE_BY = 10
PAGINATOR_ADJ = 5
BREADCRUMB_SEPARATOR = '&raquo;'

#################
# DJANGO ASSETS #
#################
ASSETS_DEBUG = local_settings.ASSETS_DEBUG
ASSETS_UPDATER="timestamp"
#ASSETS_AUTO_CREATE
#ASSETS_EXPIRE = 'filename'

######################
# COMMENTS FRAMEWORK #
######################
AKISMET_API_KEY = ''
COMMENTS_HIDE_REMOVED = False
PROFANITIES_LIST = ( 'asshat', 'asshead', 'asshole', 'cunt', 'fuck', 'gook', 'nigger', 'shit', )

###########
# ARCHIVE #
###########

ARCHIVES = (
	('djangoplicity.media.models.Image','djangoplicity.media.options.ImageOptions'),
	('djangoplicity.media.models.Video','djangoplicity.media.options.VideoOptions'),
	('djangoplicity.releases.models.Release','djangoplicity.releases.options.ReleaseOptions'),		    
)

ARCHIVE_EMBARGO_LOGIN = ('hst','vxiofpia')
ARCHIVE_EMAIL_SENDER = "ESA/Hubble Information Centre <hubble@eso.org>" 

ARCHIVE_RESOURCE_FIELDS = False
ARCHIVE_URL_QUERY_PREFIX = 'archive'
ARCHIVE_URL_DETAIL_PREFIX = ''
ARCHIVE_URL_FEED_PREFIX = 'feed'
ARCHIVE_URL_SEARCH_PREFIX = 'search'
ARCHIVE_PAGINATOR_PREFIX = 'page'
ARCHIVE_ICON_PATH = 'icons/'
ARCHIVE_ROOT = 'archives/'

ENABLE_ADVANCED_SEARCH = True
ADV_SEARCH_START_YEAR = 1998

ARCHIVE_AUTO_RESOURCE_DELETION = local_settings.ARCHIVE_AUTO_RESOURCE_DELETION
RELEASE_ARCHIVE_ROOT = 'archives/releases/'
IMAGES_ARCHIVE_ROOT = 'archives/images/'
IMAGECOMPARISON_ARCHIVE_ROOT = 'archives/imagecomparisons/'
VIDEOS_ARCHIVE_ROOT = 'archives/videos/'
ANNOUNCEMENTS_ARCHIVE_ROOT = 'archives/announcements/'

VIDEOS_FEATURED_SUBJECT = 'hubblecast'

#VIDEOS_SUBTITLES_FORMATS = ('hd_and_apple','medium_podcast')

DEFAULT_CREATOR = u"ESA/Hubble"  
DEFAULT_CREATOR_URL = "http://www.spacetelescope.org"
DEFAULT_CONTACT_ADDRESS = u"Karl-Schwarzschild-Strasse 2" 
DEFAULT_CONTACT_CITY = u"Garching bei München"
DEFAULT_CONTACT_STATE_PROVINCE = ""
DEFAULT_CONTACT_POSTAL_CODE= u"D-85748"
DEFAULT_CONTACT_COUNTRY = u"Germany" 
DEFAULT_RIGHTS = "Creative Commons Attribution 3.0 Unported license"
DEFAULT_PUBLISHER = u"ESA/Hubble"
DEFAULT_PUBLISHER_ID = u"vamp://esahubble"

DEFAULT_CREDIT = u"NASA &amp; ESA"

ARCHIVE_IMPORT_ROOT = local_settings.ARCHIVE_IMPORT_ROOT
PHOTOSHOP_ROOT = local_settings.PHOTOSHOP_ROOT
MP4BOX_PATH = local_settings.MP4BOX_PATH

ARCHIVE_WORKFLOWS = {
	'media.video.rename' : ('spacetelescope.workflows.media','video_rename'), 
}

VIDEO_RENAME_NOTIFY = ['mkornmes@eso.org',]

VIDEO_CONTENT_SERVERS = (
	( '', 'Default' ),
	( 'http://videos.spacetelescope.org/videos/', 'videos.spacetelescope.org' )
)

import djangoplicity.crosslinks
ARCHIVE_CROSSLINKS = djangoplicity.crosslinks.crosslinks_for_domain('spacetelescope.org')

ARCHIVE_DERIVATIVES_OVERRIDE = {
	'images' : 'new_hst',
	'videos' : 'new_hst',
}

##########
# SOCIAL #
##########
SOCIAL_FACEBOOK_TOKEN = local_settings.SOCIAL_FACEBOOK_TOKEN
SOCIAL_TWITTER_TUPLE = local_settings.SOCIAL_TWITTER_TUPLE


SOCIAL_FACEBOOK_WALL = 'http://www.facebook.com/hubbleESA?sk=wall'

#########
# FEEDS #
#########
FEED_SETTINGS_MODULE = 'spacetelescope.feed_settings'

############
# REPORTS  #
############
REPORTS_DEFAULT_FORMATTER = 'html'
REPORT_REGISTER_FORMATTERS = True

##########	
# CELERY #
##########
import djcelery
djcelery.setup_loader()

CELERY_IMPORTS = [
	"djangoplicity.archives.contrib.security.tasks" ,
	"djangoplicity.celery.tasks",
]

# Message routing
CELERY_DEFAULT_QUEUE = "celery"
CELERY_DEFAULT_EXCHANGE = "celery"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "celery"
CELERY_QUEUES = {
    "celery": {
        "exchange": "celery",
        "exchange_type": "direct",
        "binding_key": "celery"},
    "photoshop": {
        "exchange": "photoshop",
        "exchange_type": "direct",
        "binding_key": "photoshop"},
}
CELERY_ROUTES = {
	"media.image_derivatives" : { "queue" : "photoshop" }
}

## Broker settings.
BROKER_HOST = local_settings.BROKER_HOST
BROKER_PORT = 5672
BROKER_USER = local_settings.BROKER_USER
BROKER_PASSWORD = local_settings.BROKER_PASSWORD
BROKER_VHOST = local_settings.BROKER_VHOST
BROKER_USE_SSL = local_settings.BROKER_USE_SSL

# Task result backend
CELERY_RESULT_BACKEND = "amqp"

# AMQP backend settings 
CELERY_RESULT_SERIALIZER = "json"
CELERY_AMQP_TASK_RESULT_EXPIRES = 3600

# Task execution
CELERY_TASK_SERIALIZER='json'
CELERY_IGNORE_RESULT = False
CELERY_DISABLE_RATE_LIMITS = True

# Error email 
CELERY_SEND_TASK_ERROR_EMAILS = False

# Events
CELERY_SEND_EVENTS = True

# Logging
CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_ALWAYS_EAGER=local_settings.CELERY_ALWAYS_EAGER

# Beat
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

##############
# JavaScript #
##############
TINYMCE_JS = "djangoplicity/js/tiny_mce_v3392/tiny_mce.js"
TINYMCE_JQUERY_JS = "djangoplicity/js/tiny_mce_v3392/jquery.tinymce.js"
JQUERY_JS = "djangoplicity/js/jquery-1.4.2.min.js"
ZCLIPBOARD_JS = "djangoplicity/js/ZeroClipboard.js"
JQUERY_UI_JS = "djangoplicity/js/jquery-ui-1.8.1.custom.min.js"
JQUERY_UI_CSS = "djangoplicity/css/ui-lightness/jquery-ui-1.8.1.custom.css"
DJANGOPLICITY_ADMIN_CSS = "djangoplicity/css/admin.css"
DJANGOPLICITY_ADMIN_JS = "djangoplicity/js/admin.js"
SUBJECT_CATEGORY_CSS = "djangoplicity/css/widgets.css"
SHADOWBOX_JS = "djangoplicity/shadowbox3/shadowbox.js"
SHADOWBOX_CSS = "djangoplicity/shadowbox3/shadowbox.css"
SWFOBJECT_JS = "djangoplicity/js/swfobject.js"

REGEX_REDIRECTS = (
#	( re.compile( '/hubbleshop/webshop/webshop\.php\?show=sales&section=(books|cdroms)' ), '/shop/category/\g<1>/' ),
	( re.compile( '/about/history/sm4blog/(.+)' ), '/static/sm4blog/\g<1>' ),
	( re.compile( '/news/(doc|pdf|text)/(.+)' ), '/static/archives/releases/\g<1>/\g<2>' ),
	( re.compile( '/news/(science_paper)/(.+)' ), '/static/archives/releases/science_papers/\g<1>' ),
	( re.compile( '/images/html/([a-z0-9-_]+)\.html' ), '/images/\g<1>/' ),
	( re.compile( '/videos/(vodcast|hd1080p_screen|hd1080p_broadcast|hd720p_screen|hd720p_broadcast|h264|broadcast)/(.+)' ), '/static/archives/videos/\g<1>/\g<2>' ),
	( re.compile( '/images/html/zoomable/([a-z0-9-_]+).html' ), '/images/\g<1>/zoomable/' ),
	( re.compile( '/videos/html/mov/(320px|180px)/([a-z0-9-_]+).html' ), '/videos/\g<2>/' ),
	( re.compile( '/bin/videos.pl\?(searchtype=news&)?string=([a-z0-9-_]+)' ), '/videos/?search=\g<2>' ),
	( re.compile( '/bin/images.pl\?(searchtype=news&)?string=([a-z0-9-_]+)' ), '/images/?search=\g<2>' ),
	( re.compile( '/about/further_information/(brochures|books|newsletters)/(pdf|pdfsm)/(.+)' ), '/static/archives/\g<1>/\g<2>/\g<3>' ),
	( re.compile( '/bin/calendar.pl' ), '/extras/calendars/' ),
	( re.compile( '/bin/calendar.pl\?string=(\d+)' ), '/extras/calendars/archive/year/\g<1>/' ),
	( re.compile( '/bin/images.pl\?embargo=0&viewtype=standard&searchtype=freesearch&lang=en&string=(.+)' ), '/images/?search=\g<1>' ),
	( re.compile( '/bin/images.pl\?searchtype=freesearch&string=(.+)' ), '/images/?search=\g<1>' ),
	( re.compile( '/bin/images.pl\?searchtype=top100' ), '/images/archive/top100/' ),
	( re.compile( '/bin/images.pl\?searchtype=wallpaper' ), '/images/archive/wallpapers/' ),
	( re.compile( '/bin/news.pl\?string=([a-z0-9-_]+)' ), '/news/\g<1>/' ),
	( re.compile( '/goodies/printlayouts/html/([a-z0-9-_]+).html' ), '/news/\g<1>/' ),
	( re.compile( '/images/archive/freesearch/([^/]+)/viewall/\d+' ), '/images/?search=\g<1>' ),
	( re.compile( '/images/archive/topic/([^/]+)/(|standard)/(\d+)?' ), '/images/archive/category/\g<1>/' ),
	( re.compile( '/images/archive/wallpaper/(.+)' ), '/images/archive/wallpapers/' ),
	( re.compile( '/kidsandteachers/education/lowres_pdf/([a-z0-9-_]+)\.pdf' ), '/static/archives/education/pdfsm/\g<1>.pdf' ),
	( re.compile( '/projects/python-xmp-toolkit/(.*)' ), '/static/projects/python-xmp-toolkit/\g<1>' ),
	( re.compile( '/videos/archive/topic/([^/]+)/(|standard|viewall)/(\d+)?' ), '/videos/archive/category/\g<1>/' ),
	( re.compile( '/videos/html/mpeg/320px/([a-z0-9-_]+).html' ), '/videos/\g<1>/' ),
	( re.compile( '/videos/scripts/(.+)' ), '/static/archives/videos/script/\g<1>' ),
)

SITE_DOMAIN = "www.spacetelescope.org"

##################
# django-tinymce #
##################
TINYMCE_JS_URL = STATIC_URL + "js/tiny_mce/tiny_mce.js"
TINYMCE_JS_ROOT = STATIC_ROOT + "js/tiny_mce"
TINYMCE_DEFAULT_CONFIG = {
	"mode" : "textareas",
	"theme" : "advanced",
	"plugins" : "style,layer,table,advimage,insertdatetime,searchreplace,contextmenu,paste,fullscreen,visualchars,nonbreaking",
	"theme_advanced_buttons1" : "fullscreen,code,cleanup,|,cut,copy,paste,pastetext,pasteword,|,search,replace,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect",
	"theme_advanced_buttons2" : ",bold,italic,underline,strikethrough,|,bullist,numlist,|,outdent,indent,|,undo,redo,|,link,unlink,anchor,image,media,charmap,|,forecolor,backcolor|,styleprops,|,nonbreaking",
	"theme_advanced_buttons3" : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,insertdate,inserttime,|,insertlayer,moveforward,movebackward,absolute",
	"theme_advanced_toolbar_location" : "top",
	"theme_advanced_toolbar_align" : "left",
	"theme_advanced_statusbar_location" : "bottom",
	"extended_valid_elements" : "a[name|class|href|target|title|onclick],img[usemap|class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name|style],hr[class|width|size|noshade],span[class|align|style],script[language|type|src],object[width|height|classid|codebase|data|type|id|class|style],param[name|value],embed[src|type|width|height|flashvars|wmode|style],iframe[src|width|height|frameborder|marginheight|marginwidth|align]",
	"editor_selector" : "vRichTextAreaField",
	"media_strict" : False,
	#//relative_urls : False,
	#//remove_script_host : True,
	#//urlconverter_callback : "url_converter"
	"convert_urls" : False,
	"gecko_spellcheck" : True,
} 
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False
TINYMCE_FILEBROWSER = False


###########
# LOGGING #
###########
LOGGING = {
	'version' : 1,
	'disable_existing_loggers' : True,
	'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'default': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'default'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html' : True,
        },
        'file' : {
			'level' : 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'formatter' : 'default',
			'filename' : os.path.join( LOG_DIR, "djangoplicity.log" ), 
			'maxBytes' : 50 * 1024 * 1024, 
			'backupCount' : 3,
		}
    },
    'loggers': {
        'django': {
            'handlers': local_settings.LOGGING_HANDLER,
            'propagate': True,
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'djangoplicity': {
            'handlers': local_settings.LOGGING_HANDLER,
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django.db.backends' : {
			'handlers': local_settings.LOGGING_HANDLER if DEBUG_SQL else ['null'],
            'propagate': False,
            'level': 'DEBUG' if DEBUG_SQL else 'INFO',
		},
		'sslurllib' : {
			'handlers' : ['null',],
			'propagate': False,
		},
		'django_auth_ldap' : {
			'handlers': local_settings.LOGGING_HANDLER,
            'propagate': True,
            'level': 'DEBUG' if DEBUG else 'INFO',
		}
    },
}

###################
# REPORTLAB FONTS #
###################
from reportlab import rl_config
rl_config.TTFSearchPath.append( PRJBASE + "/fonts/" )

####################
# SOUTH MIGRATIONS #
####################
DATABASE_STORAGE_ENGINE="MyISAM"

SOUTH_TESTS_MIGRATE = local_settings.SOUTH_TESTS_MIGRATE
SOUTH_MIGRATION_MODULES = {
    'redirects': 'ignore', # We are using django.redirects and not djangoplicity.redirects where the migration is stored.
}


# ======================================================================
# SITE SPECIFIC SECTIONS 
# ======================================================================

###########
# SATCHMO #
###########
SHOP_CONF = {
	'DEFAULT_NAVISION_JOB' : '050',
	'DEFAULT_NAVISION_JSP' : 8900,
	'DEFAULT_NAVISION_ACCOUNT' : '50.030',
	'ORDER_FILE_PREFX' : "hb",
	'ARCHIVE_DEFAULTS' : {
		'djangoplicity.products.models.Poster' : { 'ACCOUNT' : '50.050', },
		'djangoplicity.products.models.PostCard' : { 'ACCOUNT' : '50.050', },
		'djangoplicity.products.models.Merchandise' : { 'ACCOUNT' : '50.050', },
		'djangoplicity.products.models.CDROM' : { 'ACCOUNT' : '50.050', },
		'djangoplicity.products.models.Calendar' : { 'ACCOUNT' : '50.050', },
		'djangoplicity.products.models.ConferenceItem' : { 'ACCOUNT' : '50.230', },
		'djangoplicity.products.models.Sticker' : { 'ACCOUNT' : '50.050', },
	}
}


import os
DIRNAME = os.path.abspath( os.path.dirname( __file__ ) )
LOCAL_DEV = True

MIDDLEWARE_CLASSES += ( 
					"threaded_multihost.middleware.ThreadLocalMiddleware",
					#"satchmo_store.shop.SSLMiddleware.SSLRedirect", 
					)

TEMPLATE_CONTEXT_PROCESSORS += ( 'satchmo_store.shop.context_processors.settings', )

AUTHENTICATION_BACKENDS += ( 'satchmo_store.accounts.email-auth.EmailBackend', )

from django.conf.urls.defaults import patterns, include
SATCHMO_SETTINGS = {
                    'SHOP_BASE' : '/shop',
                    'MULTISHOP' : False,
                    'SSL' : True,
#                    'SHOP_URLS' : patterns('',
#										( r'^checkout/', 'spacetelescope.views.shop_closed' ),
#								)
                    }



SITE_NAME = "Hubbleshop"
SITE_DOMAIN = "www.spacetelescope.org"
LOGDIR = LOG_DIR
LOGFILE = 'satchmo.log'
CHECKOUT_SSL=True

L10N_SETTINGS = {
  'currency_formats' : {
     'EURO' : {'symbol': u'€', 'positive' : u"€ %(val)0.2f", 'negative': u"€ (%(val)0.2f)", 'decimal' : ','},
  },
  'default_currency' : 'EURO',
  'show_admin_translations': False,
  'allow_translation_choice': False,
}

LIVESETTINGS_OPTIONS = {   
	1: { 
		'DB' : False, 
		'SETTINGS' : { 
		    u'LANGUAGE': {   
				u'CURRENCY': u'\u20ac',
				u'SHOW_TRANSLATIONS': u'False'
			},
            u'PAYMENT': {
				u'COUNTRY_MATCH': u'False',
                u'MINIMUM_ORDER': u'2.99',
                #u'ORDER_EMAIL_EXTRA': u'distribution@spacetelescope.org',
                u'ORDER_EMAIL_OWNER': u'True',                
                u'MODULES': u'["PAYMENT_COPOSWEB"]'
            },
            u'PAYMENT_DUMMY': {
				u'CREDITCHOICES': u'["Visa", "Mastercard", "Discover", "American Express"]'
			},
            u'PRODUCT': {   
				u'IMAGE_DIR': u'satchmoimages',
				u'MEASUREMENT_SYSTEM': u'["metric"]',
				# Note the string below is too long to store in the database since PRODUCT_TYPES is not a LongSetting
				# Therefore it must be configured here!
				u'TRACK_INVENTORY': u'False',
				u'NUM_PAGINATED': u'10',
				u'NUM_DISPLAY': u'20',
			},
            u'SHIPPING': {   
				#u'PER_DAYS': u'1 - 3 business days',
				#u'PER_SERVICE': u'Deutsche Post/DHL',
				u'SELECT_CHEAPEST': u'False',
				u'HIDING': u'NO',
				u'MODULES': u'["shipping.modules.tieredweight","djangoplicity.archives.contrib.satchmo.esoshipping.officedelivery","djangoplicity.archives.contrib.satchmo.esoshipping.pickup"]',
			},
            u'TAX' : {
				u'PRODUCTS_TAXABLE_BY_DEFAULT' :u'False',
				u'TAX_SHIPPING' : u'False', 
			},
            u'SHOP': {
				u'REQUIRED_BILLING_DATA': u'["email", "first_name", "last_name", "phone", "street1", "city", "postal_code", "country"]',
				u'ENFORCE_STATE': u'False',
				u'SHOW_SITE': u'False',
				u'LOGO_URI': u'http://www.spacetelescope.org/static/archives/logos/screen/eso_colour.jpg',
			},
            u'PAYMENT_COPOSWEB': {
				u'USER_TEST': u'testeso',
				u'PASSWORD_TEST': u'Kw6&gHKi',
				u'LIVE_CONFIG_FILE' : local_settings.COPOSWEB_CONFIG_INI,
				u'CAPTURE': u'True',
				u'LIVE': u'True' if local_settings.LIVE else u'False',
				u'EXTRA_LOGGING': u'True',
			},
		}
	}
}

ORDER_PREFIX = local_settings.ORDER_PREFIX
LIVE = local_settings.LIVE
SHOP_PICKUP_LOCATIONS = (
	{ 'id' : 'PUP1', 
	  'name' : 'ESO HQ',
	  'desc' : _( "Self-pickup/ESO HQ in Munich, Germany" ), 
	  'method' : _("Pickup (9-17 CET/CEST) at ESO HQ Reception,"),
	  'delivery' : _("Karl-Schwarzschild-Str. 2, 85748 Garching, GERMANY"),
	},
)