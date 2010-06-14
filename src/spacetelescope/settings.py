# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

# Django settings for website project
# ------------------------------------
# Note most deployment specific settings are imported
# from the settings.ini file.
#

from djangoconfutils.ini_locator import locate_ini_config
import re

config = locate_ini_config( 'spacetelescope', 'settings' )

#############################
# ENVIRONMENT CONFIGURATION #
#############################
PRJBASE = config.get('DEFAULT','PRJBASE')
PRJNAME = 'spacetelescope.org'
DJANGOPLICITY_ROOT = config.get('djangoplicity', 'ROOT' )
LOG_DIR = config.get('djangoplicity','LOG_DIR') if config.has_option('djangoplicity', 'LOG_DIR') else "/tmp"

if config.has_option('environment', 'ENABLE_SSL'):
	ENABLE_SSL = config.getboolean('environment','ENABLE_SSL')
else:
	ENABLE_SSL = False
	
GA_ID = "UA-2368492-6"

###################
# ERROR REPORTING #
###################
INTERNAL_IPS = ('127.0.0.1',)

SITE_ENVIRONMENT = config.get('environment','SITE_ENVIRONMENT') if config.has_option('environment','SITE_ENVIRONMENT') else 'local'
DEBUG = config.getboolean('environment','DEBUG')
DEBUG_SQL = config.getboolean('environment','DEBUG_SQL') if config.has_option('environment','DEBUG_SQL') else False
DEBUG_PROFILER = config.getboolean('environment','DEBUG_PROFILER') if config.has_option('environment','DEBUG_PROFILER') else False
DEBUG_TOOLBAR = config.getboolean('environment','DEBUG_TOOLBAR') if config.has_option('environment','DEBUG_TOOLBAR') else False
TEMPLATE_DEBUG = config.getboolean('environment','TEMPLATE_DEBUG')
SEND_BROKEN_LINK_EMAILS = config.getboolean('environment','SEND_BROKEN_LINK_EMAILS')

ADMINS = tuple(config.items('admins'))
MANAGERS = ADMINS

SERVE_STATIC_MEDIA = config.getboolean('environment', 'SERVE_STATIC_MEDIA')

if SERVE_STATIC_MEDIA:
	STATIC_MEDIA_PREFIX = config.get('environment', 'STATIC_MEDIA_PREFIX')
	
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
DATABASE_ENGINE 	= config.get('database', 'DATABASE_ENGINE')
DATABASE_NAME 		= config.get('database', 'DATABASE_NAME')
DATABASE_USER 		= config.get('database', 'DATABASE_USER')
DATABASE_PASSWORD 	= config.get('database', 'DATABASE_PASSWORD')
DATABASE_HOST 		= config.get('database', 'DATABASE_HOST')
DATABASE_PORT 		= config.get('database', 'DATABASE_PORT')
DATABASE_OPTIONS	= {
	# Uncomment following line when creating tables to ensure
	# InnoDB tables are created.
	#"init_command": "SET storage_engine=INNODB",
}

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
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Default date and time formats (con be overridden by locale)
DATE_FORMAT = 'j M Y'
DATE_LONG_FORMAT = 'j F Y'
DATETIME_FORMAT = 'M j, Y, H:i T'
DATETIME_LONG_FORMAT = 'M j, Y y, H:i T'
MONTH_DAY_FORMAT = 'F j'
TIME_FORMAT = 'H:i T'
YEAR_MONTH_FORMAT = 'F Y'
WIDGET_FORMAT = "j/m/Y"

###############
# MEDIA SETUP #
###############
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = config.get('media', 'MEDIA_ROOT')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = config.get('media', 'MEDIA_URL')


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = config.get('media', 'ADMIN_MEDIA_PREFIX')

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.get('secrets', 'SECRET_KEY')
CSRF_MIDDLEWARE_SECRET = config.get('secrets', 'CSRF_MIDDLEWARE_SECRET')

##########
# CACHE  #
##########
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_BACKEND = config.get('cache', 'CACHE_BACKEND')
CACHE_MIDDLEWARE_KEY_PREFIX = config.get('cache', 'CACHE_MIDDLEWARE_KEY_PREFIX')
CACHE_KEY_PREFIX = config.get('cache', 'CACHE_KEY_PREFIX') if config.has_option('cache', 'CACHE_KEY_PREFIX') else ''
CACHE_PREFIX = CACHE_KEY_PREFIX 
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_TEMPLATES = config.getboolean('cache', 'CACHE_TEMPLATES')
CACHE_TIMEOUT = 60*5

USE_ETAGS = True

#############
# TEMPLATES #
#############
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.request',
	'django.core.context_processors.auth',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
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
	
ENABLE_REDIRECT_MIDDLEWARE = config.getboolean('environment','ENABLE_REDIRECT_MIDDLEWARE') if config.has_option('environment','ENABLE_REDIRECT_MIDDLEWARE') else False


REDIRECT_MIDDLEWARE_URI = config.get('environment','REDIRECT_MIDDLEWARE_URI') if config.has_option('environment','REDIRECT_MIDDLEWARE_URI') else ''	

		

MIDDLEWARE_CLASSES += (
	# Enables session support
	'django.contrib.sessions.middleware.SessionMiddleware', # Request/Response (db)
	
    # Adds the user attribute, representing the currently-logged-in user, to every incoming 
    # HttpRequest object. 
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Request
    
    # - Forbids access to user agents in the DISALLOWED_USER_AGENTS setting
    # - Performs URL rewriting based on the APPEND_SLASH and PREPEND_WWW settings.
    # - Handles ETags based on the USE_ETAGS setting.
    'django.middleware.common.CommonMiddleware', # Request/Response
    
    # Logging of exceptions in database.
    'djangodblog.DBLogMiddleware', # Exception
	
)


if ENABLE_REDIRECT_MIDDLEWARE:
	MIDDLEWARE_CLASSES += (
		'djangoplicity.contrib.redirects.middleware.SinkRedirectMiddleware',
		)

MIDDLEWARE_CLASSES += (
	# Module for URL redirection. 
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware', # Response
	
	# Module for URL redirection based on regular expressions
	'djangoplicity.utils.middleware.RegexRedirectMiddleware', # Response
	
	# Djangoplicity static pages
	'djangoplicity.pages.middleware.PageFallbackMiddleware', # Response
)

INSTALLED_APPS = (
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
	#'djangoplicity.cache', 
	'djangoplicity.media',
	'djangoplicity.jobs',
	'django.contrib.redirects',
	'djangoplicity.announcements',
	'djangoplicity.releases',
	'djangoplicity.search',
	'djangoplicity.metadata',
	'djangoplicity',
	'djangoplicity.authtkt',
	'djangoplicity.google',
	'spacetelescope',
	'celery',
	'mptt',
	'djangodblog',
	'django_extensions',
	'django_assets',
	'spacetelescope.archives',	
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
)


if DEBUG_TOOLBAR:
	INSTALLED_APPS += (
		'debug_toolbar',
	)

############
# SESSIONS #
############
SESSION_ENGINE=config.get('sessions', 'SESSION_ENGINE') if config.has_option('sessions', 'SESSION_ENGINE') else 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE=config.getint('sessions', 'SESSION_COOKIE_AGE') if config.has_option('sessions', 'SESSION_COOKIE_AGE') else 86400
SESSION_COOKIE_DOMAIN=config.get('sessions', 'SESSION_COOKIE_DOMAIN') if config.has_option('sessions', 'SESSION_COOKIE_DOMAIN') else None

################
# FILE UPLOADS #
################
FILE_UPLOAD_TEMP_DIR = config.get('djangoplicity','TMP_DIR') if config.has_option('djangoplicity', 'TMP_DIR') else None
FILE_UPLOAD_PERMISSIONS = 0666
#FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 <-- default 

#########
# EMAIL #
#########
SERVER_EMAIL = config.get('email', 'SERVER_EMAIL')
DEFAULT_FROM_EMAIL = config.get('email', 'DEFAULT_FROM_EMAIL')
EMAIL_HOST = config.get('email', 'EMAIL_HOST')
EMAIL_HOST_PASSWORD = config.get('email', 'EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = config.get('email', 'EMAIL_HOST_USER')
EMAIL_PORT = config.get('email', 'EMAIL_PORT')
EMAIL_USE_TLS = config.get('email', 'EMAIL_USE_TLS')
EMAIL_SUBJECT_PREFIX = config.get('email', 'EMAIL_SUBJECT_PREFIX') if config.has_option('email','EMAIL_SUBJECT_PREFIX') else '[Django]'

##################
# AUTHENTICATION #
##################
AUTHENTICATION_BACKENDS = ( 'django.contrib.auth.backends.ModelBackend', )
#AUTH_PROFILE_MODULE = ''
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

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
if config.has_option('gis', 'GEOIP_PATH'):
	GEOIP_PATH = config.get('gis', 'GEOIP_PATH')

if config.has_option('gis', 'GEOIP_LIBRARY_PATH'):
	GEOIP_LIBRARY_PATH = config.get('gis', 'GEOIP_LIBRARY_PATH')

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

#####################
# DJANGO BATCHADMIN #
#####################
#BATCHADMIN_MEDIA_PREFIX	
BATCHADMIN_JQUERY_JS = "js/jquery-1.2.6.min.js"

#################
# DJANGO ASSETS #
#################
#ASSETS_DEBUG
#ASSETS_UPDATER
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

ARCHIVE_RESOURCE_FIELDS = False
ARCHIVE_URL_QUERY_PREFIX = 'archive'
ARCHIVE_URL_DETAIL_PREFIX = ''
ARCHIVE_URL_FEED_PREFIX = 'feed'
ARCHIVE_PAGINATOR_PREFIX = 'page'
ARCHIVE_ICON_PATH = 'icons/'

RELEASE_ARCHIVE_ROOT = 'archives/releases/'
IMAGES_ARCHIVE_ROOT = 'archives/images/'
VIDEOS_ARCHIVE_ROOT = 'archives/videos/'

DEFAULT_CREATOR = u"ESA/Hubble"  
DEFAULT_CREATOR_URL = "http://www.spacetelescope.org"
DEFAULT_CONTACT_ADDRESS = u"Karl-Schwarzschild-Strasse 2" 
DEFAULT_CONTACT_CITY = u"Garching bei München"
DEFAULT_CONTACT_STATE_PROVINCE = ""
DEFAULT_CONTACT_POSTAL_CODE= u"D-85748"
DEFAULT_CONTACT_COUNTRY = u"Germany" 
DEFAULT_RIGHTS = ""
DEFAULT_PUBLISHER = u"ESA/Hubble"
DEFAULT_PUBLISHER_ID = u"vamp://esahubble"

ARCHIVE_IMPORT_ROOT = config.get('media','ARCHIVE_IMPORT_ROOT') if config.has_option('media','ARCHIVE_IMPORT_ROOT')  else '/Volumes/webdocs/importi'
ARCHIVE_WORKFLOWS = {
	'media.video.rename' : ('eso.workflows.media','video_rename'), 
}

VIDEO_RENAME_NOTIFY = ['mkornmes@eso.org',]

VIDEO_CONTENT_SERVERS = (
	( '', 'Default' ),
	( 'http://videos.spacetelescope.org/videos/', 'videos.spacetelescope.org' )
)

"""
format:
ARCHIVE_CROSSLINKS = {
	'archive urlname_prefix': (('display name 1','url1'),
							('display name 2','url2'),...),
							
							}
"""
ARCHIVE_CROSSLINKS = {
			'announcements': (('eso.org','http://www.eso.org/public/announcements/'),),
			'releases': (('eso.org','http://www.eso.org/public/news/'),
						 ('iau.org', 'http://www.iau.org/public_press/news/'),
						 ('astronomy2009.org', 'http://www.astronomy2009.org/news/pressreleases/'),
						),
			'images': (('eso.org','http://www.eso.org/public/images/'),
						 ('iau.org', 'http://www.iau.org/public_press/images/'),
						 ('astronomy2009.org', 'http://www.astronomy2009.org/resources/multimedia/images/'),
						),
			'videos': (('eso.org','http://www.eso.org/public/videos/'),
					   ('astronomy2009.org', 'http://www.astronomy2009.org/resources/multimedia/videos/'),
					   ),
			'potw': (('eso.org','http://www.eso.org/public/images/potw/'),
						),
			'posters': (('eso.org','http://www.eso.org/public/outreach/products/posters/index_sale.html'),
						('astronomy2009.org','http://www.astronomy2009.org/resources/posters/'),
						),
			'books': (('eso.org','http://www.eso.org/public/outreach/products/books/'),
					  ('astronomy2009.org','http://www.astronomy2009.org/resources/books/'),
					  ('iau.org','http://www.iau.org/science/publications/iau/'),
						),
			'brochures': (('eso.org','http://www.eso.org/public/outreach/products/brochures/'),
						  ('astronomy2009.org','http://www.astronomy2009.org/resources/brochures/'),
						),
			'calendars': (('eso.org','http://www.eso.org/public/outreach/products/calendars/'),
						),
			'education': (('eso.org','http://www.eso.org/public/outreach/eduoff/materials.html'),
						  ('astronomy2009.org','http://www.astronomy2009.org/resources/educational/'),
						),
			'newsletters':(('eso.org','http://www.eso.org/sci/enews/archive.html'),
						),
			'postcards': (('eso.org','http://www.eso.org/public/outreach/products/postcards/'),
						),
			'logos': (('eso.org','http://www.eso.org/public/outreach/products/logos/eso/index.html'),
						('astronomy2009.org','http://www.astronomy2009.org/resources/branding/'),
						('iau.org','http://www.iau.org/public_press/images/archive/category/logos/'),
						),	
			'conferenceposters': (
						('astronomy2009.org','http://www.astronomy2009.org/resources/posters/'),
						),	
			'presentations': (
						('eso.org','http://www.eso.org/public/outreach/products/presentations/'),
						('astronomy2009.org','http://www.astronomy2009.org/resources/presentations/'),
						),						
			
						
					  }


# FEEDS SETTINGS MODULE
FEED_SETTINGS_MODULE = 'spacetelescope.feed_settings'

############
# REPORTS  #
############
REPORTS_DEFAULT_FORMATTER = 'html'
REPORT_REGISTER_FORMATTERS = True

########	
# AMQP #
########
AMQP_SERVER = config.get('amqp', 'AMQP_SERVER') if config.has_option('amqp', 'AMQP_SERVER') else None
AMQP_PORT = config.get('amqp', 'AMQP_PORT') if config.has_option('amqp', 'AMQP_PORT') else None
AMQP_USER = config.get('amqp', 'AMQP_USER') if config.has_option('amqp', 'AMQP_USER') else None
AMQP_PASSWORD = config.get('amqp', 'AMQP_PASSWORD') if config.has_option('amqp', 'AMQP_PASSWORD') else None
AMQP_VHOST = config.get('amqp', 'AMQP_VHOST') if config.has_option('amqp', 'AMQP_VHOST') else None


CELERY_BACKEND = config.get('celery','CELERY_BACKEND') if config.has_option('celery','CELERY_BACKEND') else None
CELERY_CACHE_BACKEND =  config.get('celery','CELERY_CACHE_BACKEND') if config.has_option('celery','CELERY_CACHE_BACKEND') else None
CELERY_AMQP_EXCHANGE = config.get("celery",'CELERY_AMQP_EXCHANGE') if config.has_option('celery','CELERY_AMQP_EXCHANGE') else None
CELERY_AMQP_PUBLISHER_ROUTING_KEY = config.get("celery",'CELERY_AMQP_EXCHANGE') if config.has_option('celery','CELERY_AMQP_PUBLISHER_ROUTING_KEY') else None
CELERY_AMQP_CONSUMER_QUEUE = config.get('celery',"CELERY_AMQP_CONSUMER_QUEUE") if config.has_option('celery','CELERY_AMQP_CONSUMER_QUEUE') else None
CELERY_AMQP_CONSUMER_ROUTING_KEY = config.get("celery",'CELERY_AMQP_EXCHANGE') if config.has_option('celery','CELERY_AMQP_CONSUMER_ROUTING_KEY') else None
CELERY_AMQP_EXCHANGE_TYPE = config.get('celery','CELERY_AMQP_EXCHANGE_TYPE') if config.has_option('celery','CELERY_AMQP_EXCHANGE_TYPE') else None


########
# JOBS #
########
UPDATE_JOBS_RUN_EVERY = 300

##############
# JavaScript #
##############
TINYMCE_JS = "djangoplicity/js/tiny_mce_v33/tiny_mce.js"
TINYMCE_JQUERY_JS = "djangoplicity/js/tiny_mce_v33/jquery.tinymce.js"
JQUERY_JS = "djangoplicity/js/jquery-1.4.2.min.js"
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

# ======================================================================
# SITE SPECIFIC SECTIONS 
# ======================================================================

###########
# SATCHMO #
###########
SHOP_CONF = {
	'DEFAULT_NAVISION_JOB' : '280E',
	'DEFAULT_NAVISION_JSP' : 6265,
	'ORDER_FILE_PREFX' : 'hb',
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
                    'CUSTOM_PRODUCT_MODULES' : [
											'spacetelescope.archives',
											],
					'CUSTOM_PAYMENT_MODULES' : [
											'djangoplicity.coposweb',
											],
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
  'show_translations': False,
  'allow_translations': False,
}

#import logging
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S')
#
#logging.getLogger( 'keyedcache' ).setLevel( logging.INFO )
#logging.getLogger( 'l10n' ).setLevel( logging.INFO )
#logging.info( "Satchmo Started" )

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
                u'MINIMUM_ORDER': u'3.00',
                #u'ORDER_EMAIL_EXTRA': u'distribution@spacetelescope.org',
                u'ORDER_EMAIL_OWNER': u'True',
                u'SSL': u'True',
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
				u'PRODUCT_TYPES': u'["product::ConfigurableProduct", "product::ProductVariation", "spacetelescope.archives::Book", "spacetelescope.archives::Brochure", "spacetelescope.archives::EducationalMaterial", "spacetelescope.archives::CDROM", "spacetelescope.archives::Poster", "spacetelescope.archives::TechnicalDocument", "spacetelescope.archives::Newsletter", "spacetelescope.archives::Merchandise", "spacetelescope.archives::Sticker", "spacetelescope.archives::PostCard"]',
				u'TRACK_INVENTORY': u'False',
				u'NUM_PAGINATED': u'10',
				u'NUM_DISPLAY': u'20',
			},
            u'SHIPPING': {   
				#u'PER_DAYS': u'1 - 3 business days',
				#u'PER_SERVICE': u'Deutsche Post/DHL',
				u'HIDING': u'NO',
				u'MODULES': u'["shipping.modules.tieredweight"]',
			},
            u'TAX' : {
				u'PRODUCTS_TAXABLE_BY_DEFAULT' :u'False',
				u'TAX_SHIPPING' : u'False', 
			},
            u'SHOP': {
				u'REQUIRED_BILLING_DATA': u'["email", "first_name", "last_name", "phone", "street1", "city", "postal_code", "country"]',
				u'ENFORCE_STATE': u'False',
				u'LOGO_URI': u'http://www.spacetelescope.org/about_us/logos/transparent/esa_hubble_colour_wb_gen.png',
			},
            u'PAYMENT_COPOSWEB': {
				u'USER_TEST': u'testeso',
				u'PASSWORD_TEST': u'Kw6&gHKi',
				u'LIVE_CONFIG_FILE' : config.get("shop","COPOSWEB_CONFIG_INI", "/etc/coposweb.ini"),
				u'CAPTURE': u'True',
				u'LIVE': u'True' if config.getboolean("shop","LIVE" ) else u'False',
				u'EXTRA_LOGGING': u'True',				
			},
		}
	}
}

ORDER_PREFIX = config.get( "shop", "ORDER_PREFIX", "hb" )