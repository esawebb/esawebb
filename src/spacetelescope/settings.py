# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from __future__ import absolute_import

from djangoplicity.settings import import_settings

from celery.schedules import crontab
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
ALLOW_SSL = local_settings.ALLOW_SSL
GA_ID = "UA-2368492-6"
FACEBOOK_APP_ID = "144508505618279"

#####################
# CONFIG GENERATION #
#####################
SHORT_NAME = local_settings.SHORT_NAME
WEBSERVERS = local_settings.WEBSERVERS
SSL_ASSETS_PREFIX = local_settings.SSL_ASSETS_PREFIX


###################
# ERROR REPORTING #
###################
class internal_ips( list ):
	"""
	INTERNAL_IPS container that allows more specific check if an IP is an internal IP.

	Each entry must be a complete ( a.b.c.d ) or partial ( a.b.c. ) IP address. If
	an entry is prefixed with tilde ( ~ ) it means the IP address is excluded. This allows
	you e.g include the entire range 134.171. but exclude certain subnets and specific IP
	addresses.
	"""
	def __contains__( self, key ):
		is_internal = False
		for ip in self:
			if ip[0] == '~':
				if key.startswith( ip[1:] ):
					return False
			else:
				if key.startswith( ip ):
					is_internal = True
		return is_internal

INTERNAL_IPS = internal_ips( [
	'127.0.0.1',
	'134.171.',
	'~134.171.17.',
	'~134.171.86.',
	'~134.171.172.',
	'~134.171.185.',
	'~134.171.80.85',
] )

GARCHING_INTERNAL_IPS = (
	'134.171.0.0/18',
	'134.171.64.0/20',
	'127.0.0.1',
)

SITE_ENVIRONMENT = local_settings.SITE_ENVIRONMENT
DEBUG = local_settings.DEBUG
DEBUG_TOOLBAR = local_settings.DEBUG_TOOLBAR
TEMPLATE_DEBUG = local_settings.TEMPLATE_DEBUG
SEND_BROKEN_LINK_EMAILS = local_settings.SEND_BROKEN_LINK_EMAILS

ADMINS = local_settings.ADMINS
MANAGERS = ADMINS

SERVE_STATIC_MEDIA = local_settings.SERVE_STATIC_MEDIA

DEBUG_TOOLBAR_PANELS = local_settings.DEBUG_TOOLBAR_PANELS

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
# ADMIN_MEDIA_PREFIX is necessary due to satchmo current version. TODO: remove when Satchmo is upgraded
ADMIN_MEDIA_PREFIX = local_settings.ADMIN_MEDIA_PREFIX
DJANGOPLICITY_MEDIA_URL = local_settings.DJANGOPLICITY_MEDIA_URL
DJANGOPLICITY_MEDIA_ROOT = local_settings.DJANGOPLICITY_MEDIA_ROOT

MIDENTIFY_PATH = local_settings.MIDENTIFY_PATH

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
CACHE_TIMEOUT = CACHE_MIDDLEWARE_SECONDS if CACHES['default']['BACKEND'] != 'django.core.cache.backends.dummy.DummyCache' else 0  # prevents stupid error from keyecache
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
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'djangoplicity.utils.context_processors.site_environment',
	'djangoplicity.utils.context_processors.project_environment',
	'djangoplicity.utils.context_processors.google_analytics_id',
	'djangoplicity.utils.context_processors.djangoplicity_environment',
	'djangoplicity.archives.context_processors.internal_request',
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
	'django.middleware.gzip.GZipMiddleware',  # Response

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

if DEBUG_TOOLBAR:
	# Add debug toolbar to request
	MIDDLEWARE_CLASSES += (
		'debug_toolbar.middleware.DebugToolbarMiddleware',
	)

ENABLE_REDIRECT_MIDDLEWARE = local_settings.ENABLE_REDIRECT_MIDDLEWARE
REDIRECT_MIDDLEWARE_URI = local_settings.REDIRECT_MIDDLEWARE_URI


MIDDLEWARE_CLASSES += (
	# Enables session support
	'django.contrib.sessions.middleware.SessionMiddleware',  # Request/Response (db)

	# Adds the user attribute, representing the currently-logged-in user, to every incoming
	# HttpRequest object.
	'django.contrib.auth.middleware.AuthenticationMiddleware',  # Request

	# enables Messaging middleware
	'django.contrib.messages.middleware.MessageMiddleware',

)

if USE_I18N:
	MIDDLEWARE_CLASSES += (
		# Sets local for request based on URL prefix.
		'djangoplicity.translation.middleware.LocaleMiddleware',  # Request/Response
	)

MIDDLEWARE_CLASSES += (
	# - Forbids access to user agents in the DISALLOWED_USER_AGENTS setting
	# - Performs URL rewriting based on the APPEND_SLASH and PREPEND_WWW settings.
	# - Handles ETags based on the USE_ETAGS setting.
	'django.middleware.common.CommonMiddleware',  # Request/Response


	# Sets a boolean session variable INTERNAL_REQUEST if request.META['REMOTE_ADDR'] is in INTERNAL_IPS
	'djangoplicity.archives.middleware.InternalRequestMiddleware',  # Request
)


MIDDLEWARE_CLASSES += (
	# Module for URL redirection.
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware',  # Response

	# Module for URL redirection based on regular expressions
	'djangoplicity.utils.middleware.RegexRedirectMiddleware',  # Response

	# Middleware to bypass CDN when client is from Garching Intranet
	'spacetelescope.middleware.DisableInternalCDN',
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
	'django.contrib.postgres',
	'satchmo_store.shop',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.redirects',
	'django.contrib.sessions',
	'django.contrib.admin',
	'django.contrib.admindocs',
	#'django.contrib.comments',
	'django.contrib.messages',
	'django.contrib.humanize',
	'django.contrib.sitemaps',
	'djangoplicity.menus',
	'djangoplicity.reports',
	#'djangoplicity.massmailer',
	#'djangoplicity.news',
	'djangoplicity.pages',
	'djangoplicity.media',
	#'djangoplicity.contrib.redirects',
	'djangoplicity.archives',
	'djangoplicity.archives.contrib.satchmo.freeorder',
	'djangoplicity.archives.contrib.security',
	'djangoplicity.announcements',
	'djangoplicity.science',
	'djangoplicity.releases',
	'djangoplicity.products',
	'djangoplicity.metadata',
	'djangoplicity.cache',
	'djangoplicity.adminhistory',
	'djangoplicity.utils',
	'djangoplicity.celery',
	#'djangoplicity.events',
	'djangoplicity.mailinglists',
	'djangoplicity.newsletters',
	'djangoplicity.iframe',
	#'djangoplicity.contacts',
	'djangoplicity.customsearch',
	'djangoplicity.admincomments',
	'djangoplicity.simplearchives',
	#'djangoplicity.eventcalendar',
	'djangoplicity.actions',
	'djangoplicity.crawler',
	#'djangoplicity.mailer',
	#'djangoplicity.scrum',
	#'djangoplicity.kiosk.engine',
	#'djangoplicity.kiosk.slides',
	'spacetelescope',
	'spacetelescope.frontpage',
	'mptt',
	'django_extensions',
	# Satchmo
	#'registration',
	'sorl.thumbnail',
	'keyedcache',
	'livesettings',
	'satchmo_utils',
	'satchmo_store.contact',
	'product',
	'product.modules.configurable',
	'shipping',
	'payment',
	'djangoplicity.coposweb',
	'l10n',
	'tax',
	'tax.modules.no',
	'app_plugins',
	'shipping.modules.tieredweight',
	'captcha',
	'gunicorn',
	'django_ace',
	'rest_framework',
	'pipeline',
)


if DEBUG_TOOLBAR:
	INSTALLED_APPS += (
		'debug_toolbar',
	)

############
# SESSIONS #
############
SESSION_ENGINE = local_settings.SESSION_ENGINE
SESSION_COOKIE_AGE = local_settings.SESSION_COOKIE_AGE
SESSION_COOKIE_DOMAIN = local_settings.SESSION_COOKIE_DOMAIN
#TODO: remove when python 2.7 is installed on productino
SESSION_COOKIE_HTTPONLY = False


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

if local_settings.DISABLE_LDAP:
	AUTHENTICATION_BACKENDS = (
		'django.contrib.auth.backends.ModelBackend',
	)
else:
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
if not local_settings.DISABLE_LDAP:  # Ensure that module is not loaded if disabled
	import ldap
	from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType

	AUTH_LDAP_SERVER_URI = "ldaps://ldap.ads.eso.org:636/ads.eso.org"

	AUTH_LDAP_GLOBAL_OPTIONS = {
		ldap.OPT_REFERRALS: 0,
		ldap.OPT_PROTOCOL_VERSION: 3,
		ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER
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
	AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
		"dc=ads,dc=eso,dc=org",
		ldap.SCOPE_SUBTREE, "(objectClass=group)"
	)

	# Defaults:
	# - ePOD staff will get active/staff account - but no permissions.
	# - All ESO staff will get an inactive account on login - this account has to manually be activated.
	AUTH_LDAP_ALWAYS_UPDATE_USER = False  # Prevent user from being updated every time a user logs in.

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
GEOIP_PATH = local_settings.GEOIP_PATH
GEOIP_LIBRARY_PATH = local_settings.GEOIP_LIBRARY_PATH

#########
# PAGES #
#########
PAGE_TEMPLATE_CHOICES = (
	('pages/page_onecolumn.html', 'Default one column layout'),
	('pages/page_twocolumn.html', 'Default two column layout'),
	('pages/page_search.html', 'Google custom search layout')
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
ASSETS_UPDATER = "timestamp"
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

# For static media protection to be enabled, and archive must be present here
# For file import to work, the archive must be present here.
ARCHIVES = (
	('djangoplicity.media.models.Image', 'djangoplicity.media.options.ImageOptions'),
	('djangoplicity.media.models.Video', 'djangoplicity.media.options.VideoOptions'),
	('djangoplicity.media.models.VideoSubtitle', 'djangoplicity.media.options.VideoSubtitleOptions'),
	('djangoplicity.media.models.ImageComparison', 'djangoplicity.media.options.ImageComparisonOptions'),
	('djangoplicity.releases.models.Release', 'djangoplicity.releases.options.ReleaseOptions'),
	#('djangoplicity.announcements.models.Announcement','djangoplicity.announcements.options.AnnouncementOptions'),
	('djangoplicity.products.models.Application', 'djangoplicity.products.options.ApplicationOptions'),

	('djangoplicity.products.models.AnnualReport', 'djangoplicity.products.options.AnnualReportOptions'),
	('djangoplicity.products.models.Book', 'djangoplicity.products.options.BookOptions'),
	('djangoplicity.products.models.Brochure', 'djangoplicity.products.options.BrochureOptions'),
	('djangoplicity.products.models.Calendar', 'djangoplicity.products.options.CalendarOptions'),
	('djangoplicity.products.models.Media', 'djangoplicity.products.options.MediaOptions'),
	('djangoplicity.products.models.ConferenceItem', 'djangoplicity.products.options.ConferenceItemOptions'),
	#('djangoplicity.products.models.ConferencePoster','djangoplicity.products.options.ConferencePosterOptions'),
	('djangoplicity.products.models.EducationalMaterial', 'djangoplicity.products.options.EducationalMaterialOptions'),
	('djangoplicity.products.models.Exhibition', 'djangoplicity.products.options.ExhibitionOptions'),
	('djangoplicity.products.models.FITSImage', 'djangoplicity.products.options.FITSImageOptions'),
	('djangoplicity.products.models.Flyer', 'djangoplicity.products.options.FlyerOptions'),
	('djangoplicity.products.models.Handout', 'djangoplicity.products.options.HandoutOptions'),
	#('djangoplicity.products.models.Handout','djangoplicity.products.options.HandoutOptions'),
	('djangoplicity.products.models.IMAXFilm', 'djangoplicity.products.options.IMAXFilmOptions'),
	('djangoplicity.products.models.KidsDrawing', 'djangoplicity.products.options.KidsDrawingOptions'),
	('djangoplicity.products.models.Logo', 'djangoplicity.products.options.LogoOptions'),
	('djangoplicity.products.models.Apparel', 'djangoplicity.products.options.ApparelOptions'),
	('djangoplicity.products.models.Map', 'djangoplicity.products.options.MapOptions'),
	('djangoplicity.products.models.Merchandise', 'djangoplicity.products.options.MerchandiseOptions'),
	('djangoplicity.products.models.MiniSite', 'djangoplicity.products.options.MiniSiteOptions'),
	('djangoplicity.products.models.Bulletin', 'djangoplicity.products.options.BulletinOptions'),
	('djangoplicity.products.models.Stationery', 'djangoplicity.products.options.StationeryOptions'),
	('djangoplicity.products.models.ScienceInSchool', 'djangoplicity.products.options.ScienceInSchoolOptions'),
	('djangoplicity.products.models.Messenger', 'djangoplicity.products.options.MessengerOptions'),
	('djangoplicity.products.models.CapJournal', 'djangoplicity.products.options.CapJournalOptions'),
	('djangoplicity.products.models.STECFNewsletter', 'djangoplicity.products.options.STECFNewsletterOptions'),
	('djangoplicity.products.models.OnlineArt', 'djangoplicity.products.options.OnlineArtOptions'),
	('djangoplicity.products.models.OnlineArtAuthor', 'djangoplicity.products.options.OnlineArtAuthorOptions'),
	('djangoplicity.products.models.PaperModel', 'djangoplicity.products.options.PaperModelOptions'),
	('djangoplicity.products.models.PlanetariumShow', 'djangoplicity.products.options.PlanetariumShowOptions'),
	('djangoplicity.products.models.Donation', 'djangoplicity.products.options.DonationOptions'),
	('djangoplicity.products.models.PostCard', 'djangoplicity.products.options.PostCardOptions'),
	('djangoplicity.products.models.PrintedPoster', 'djangoplicity.products.options.PrintedPosterOptions'),
	('djangoplicity.products.models.ConferencePoster', 'djangoplicity.products.options.ConferencePosterOptions'),
	('djangoplicity.products.models.ElectronicPoster', 'djangoplicity.products.options.ElectronicPosterOptions'),
	('djangoplicity.products.models.Presentation', 'djangoplicity.products.options.PresentationOptions'),
	('djangoplicity.products.models.PressKit', 'djangoplicity.products.options.PressKitOptions'),
	('djangoplicity.products.models.ElectronicCard', 'djangoplicity.products.options.ElectronicCardOptions'),
	('djangoplicity.products.models.Sticker', 'djangoplicity.products.options.StickerOptions'),
	('djangoplicity.products.models.TechnicalDocument', 'djangoplicity.products.options.TechnicalDocumentOptions'),
	('djangoplicity.products.models.UserVideo', 'djangoplicity.products.options.UserVideoOptions'),
	('djangoplicity.products.models.VirtualTour', 'djangoplicity.products.options.VirtualTourOptions'),
	('djangoplicity.products.models.Model3d', 'djangoplicity.products.options.Model3dOptions'),
	('djangoplicity.newsletters.models.Newsletter', 'djangoplicity.newsletters.options.NewsletterOptions'),
)

ARCHIVE_EMBARGO_LOGIN = ('hst', 'shtenvix')
ARCHIVE_EMAIL_SENDER = "ESA/Hubble Information Centre <hubble@eso.org>"

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
NEWSLETTERS_ARCHIVE_ROOT = 'archives/newsletters/'
SCIENCEANNOUNCEMENTS_ARCHIVE_ROOT = 'archives/science/'

SHOP_NEWSLETTER_FROM = 'ESO & ESA/Hubble'

VIDEOS_FEATURED_SUBJECT = 'hubblecast'

VIDEOS_SUBTITLES_FORMATS = ('hd_and_apple', 'medium_podcast')
# List of extra formats which should be removed when importing new videos.
VIDEOS_FORMATS_REMOVE = [
	#'hd_broadcast_720p25',
]

RELEASE_LINK_PREFIX = "heic"

DEFAULT_CREATOR = u"ESA/Hubble"
DEFAULT_CREATOR_URL = "http://www.spacetelescope.org"
DEFAULT_CONTACT_ADDRESS = u"Karl-Schwarzschild-Strasse 2"
DEFAULT_CONTACT_CITY = u"Garching bei M√ºnchen"
DEFAULT_CONTACT_STATE_PROVINCE = ""
DEFAULT_CONTACT_POSTAL_CODE = u"D-85748"
DEFAULT_CONTACT_COUNTRY = u"Germany"
DEFAULT_RIGHTS = "Creative Commons Attribution 4.0 International License"
DEFAULT_PUBLISHER = u"ESA/Hubble"
DEFAULT_PUBLISHER_ID = u"esahubble"

DEFAULT_CREDIT = u"NASA &amp; ESA"

ARCHIVE_IMPORT_ROOT = local_settings.ARCHIVE_IMPORT_ROOT
MP4BOX_PATH = local_settings.MP4BOX_PATH

ARCHIVE_WORKFLOWS = {
	'media.video.rename': ('spacetelescope.workflows.media', 'video_rename'),
}

VIDEO_RENAME_NOTIFY = ['hzodet@eso.org', 'mkornmes@eso.org']

import djangoplicity.crosslinks
ARCHIVE_CROSSLINKS = djangoplicity.crosslinks.crosslinks_for_domain('spacetelescope.org')

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

##########################
# PHOTOSHOP CELERYWORKER #
##########################
PHOTOSHOP_ROOT = local_settings.PHOTOSHOP_ROOT

# For several djangoplicity installations to share a common
# photoshop server, they must direct tasks to a common broker/vhost.
# If the photoshop server is only to generate image derivatives for
# one djangoplicity installation this setting can just be set to
# none (which means the default broker for celery is used).
PHOTOSHOP_BROKER = local_settings.PHOTOSHOP_BROKER

##########
# CELERY #
##########

CELERY_IMPORTS = [
	"djangoplicity.archives.contrib.security.tasks",
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
# Directs all image generation tasks to the "photoshop" queue
CELERY_ROUTES = {
	"media.image_derivatives": { "queue": "photoshop" }
}

CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False

## Broker settings.
BROKER_USE_SSL = local_settings.BROKER_USE_SSL
BROKER_URL = local_settings.BROKER_URL

# Task result backend
CELERY_RESULT_BACKEND = "amqp"

# AMQP backend settings
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_RESULT_EXPIRES = 3600

# Task execution
CELERY_TASK_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False
CELERY_DISABLE_RATE_LIMITS = True

# Error email
CELERY_SEND_TASK_ERROR_EMAILS = True

# Events
CELERY_SEND_EVENTS = True

# Logging
CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_ALWAYS_EAGER = local_settings.CELERY_ALWAYS_EAGER

# File to save revoked tasks across workers restart
CELERYD_STATE_DB = "%s/tmp/celery_states" % ROOT
CELERYBEAT_SCHEDULE_FILENAME = '%s/tmp/celerybeat_schedule' % ROOT

# Define Celery periodic tasks
CELERYBEAT_SCHEDULE = {
	'mailchimp-abuse-report': {
		'task': 'newsletters.abuse_reports',
		'schedule': crontab(minute=0, hour=8, day_of_week='fri'),
	},
	'mailchimp-fetch-info': {
		'task': 'mailinglists.mailchimplist_fetch_info',
		'schedule': crontab(minute=0, hour=8),
	},
	'mailchimp-install-hooks': {
		'task': 'mailinglists.webhooks',
		'schedule': crontab(minute=50, hour=4),
	},
	'mailchimp-clean-tokens': {
		'task': 'mailinglists.clean_tokens',
		'schedule': crontab(minute=5, hour=5),
	},
	'check-content-server-resources': {
		'task': 'djangoplicity.contentserver.tasks.check_content_server_resources',
		'schedule': crontab(minute=0, hour=4),
	},
}

##############
# JavaScript #
##############
TINYMCE_JS = "djangoplicity/js/tiny_mce_v3392/tiny_mce.js"
TINYMCE_JQUERY_JS = "djangoplicity/js/tiny_mce_v3392/jquery.tinymce.js"
JQUERY_JS = "jquery/jquery-1.11.1.min.js"
JQUERY_UI_JS = "jquery-ui-1.11.1/jquery-ui.min.js"
JQUERY_UI_CSS = "jquery-ui-1.11.1/jquery-ui.min.css"
DJANGOPLICITY_ADMIN_CSS = "djangoplicity/css/admin.css"
DJANGOPLICITY_ADMIN_JS = "djangoplicity/js/admin.js"
SUBJECT_CATEGORY_CSS = "djangoplicity/css/widgets.css"

REGEX_REDIRECTS = (
#	( re.compile( '/hubbleshop/webshop/webshop\.php\?show=sales&section=(books|cdroms)' ), '/shop/category/\g<1>/' ),
	( re.compile( r'/about/history/sm4blog/(.+)' ), r'/static/sm4blog/\g<1>' ),
	( re.compile( r'/news/(doc|pdf|text)/(.+)' ), r'/static/archives/releases/\g<1>/\g<2>' ),
	( re.compile( r'/news/(science_paper)/(.+)' ), r'/static/archives/releases/science_papers/\g<1>' ),
	( re.compile( r'/images/html/([a-z0-9-_]+)\.html' ), r'/images/\g<1>/' ),
	( re.compile( r'/videos/(vodcast|hd1080p_screen|hd1080p_broadcast|hd720p_screen|hd720p_broadcast|h264|broadcast)/(.+)' ), r'/static/archives/videos/\g<1>/\g<2>' ),
	( re.compile( r'/images/html/zoomable/([a-z0-9-_]+).html' ), r'/images/\g<1>/zoomable/' ),
	( re.compile( r'/videos/html/mov/(320px|180px)/([a-z0-9-_]+).html' ), r'/videos/\g<2>/' ),
	( re.compile( r'/bin/videos.pl\?(searchtype=news&)?string=([a-z0-9-_]+)' ), r'/videos/?search=\g<2>' ),
	( re.compile( r'/bin/images.pl\?(searchtype=news&)?string=([a-z0-9-_]+)' ), r'/images/?search=\g<2>' ),
	( re.compile( r'/about/further_information/(brochures|books|newsletters)/(pdf|pdfsm)/(.+)' ), r'/static/archives/\g<1>/\g<2>/\g<3>' ),
	( re.compile( r'/bin/calendar.pl' ), r'/extras/calendars/' ),
	( re.compile( r'/bin/calendar.pl\?string=(\d+)' ), r'/extras/calendars/archive/year/\g<1>/' ),
	( re.compile( r'/bin/images.pl\?embargo=0&viewtype=standard&searchtype=freesearch&lang=en&string=(.+)' ), r'/images/?search=\g<1>' ),
	( re.compile( r'/bin/images.pl\?searchtype=freesearch&string=(.+)' ), r'/images/?search=\g<1>' ),
	( re.compile( r'/bin/images.pl\?searchtype=top100' ), r'/images/archive/top100/' ),
	( re.compile( r'/bin/images.pl\?searchtype=wallpaper' ), r'/images/archive/wallpapers/' ),
	( re.compile( r'/bin/news.pl\?string=([a-z0-9-_]+)' ), r'/news/\g<1>/' ),
	( re.compile( r'/goodies/printlayouts/html/([a-z0-9-_]+).html' ), r'/news/\g<1>/' ),
	( re.compile( r'/images/archive/freesearch/([^/]+)/viewall/\d+' ), r'/images/?search=\g<1>' ),
	( re.compile( r'/images/archive/topic/([^/]+)/(|standard)/(\d+)?' ), r'/images/archive/category/\g<1>/' ),
	( re.compile( r'/images/archive/wallpaper/(.+)' ), r'/images/archive/wallpapers/' ),
	( re.compile( r'/kidsandteachers/education/lowres_pdf/([a-z0-9-_]+)\.pdf' ), r'/static/archives/education/pdfsm/\g<1>.pdf' ),
	( re.compile( r'/projects/python-xmp-toolkit/(.*)' ), r'/static/projects/python-xmp-toolkit/\g<1>' ),
	( re.compile( r'/videos/archive/topic/([^/]+)/(|standard|viewall)/(\d+)?' ), r'/videos/archive/category/\g<1>/' ),
	( re.compile( r'/videos/html/mpeg/320px/([a-z0-9-_]+).html' ), r'/videos/\g<1>/' ),
	( re.compile( r'/videos/scripts/(.+)' ), r'/static/archives/videos/script/\g<1>' ),
)

SITE_DOMAIN = "www.spacetelescope.org"


###########
# LOGGING #
###########
LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'default': {
			'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
		},
	},
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'null': {
			'level': 'DEBUG',
			'class': 'django.utils.log.NullHandler',
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'default'
		},
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler',
			'include_html': True,
		},
		'file': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'formatter': 'default',
			'filename': os.path.join( LOG_DIR, "djangoplicity.log" ),
			'maxBytes': 50 * 1024 * 1024,
			'backupCount': 3,
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
		'django.db.backends': {
			'handlers': local_settings.LOGGING_HANDLER,
			'propagate': False,
			'level': 'INFO',
		},
		'sslurllib': {
			'handlers': ['null', ],
			'propagate': False,
		},
		'django_auth_ldap': {
			'handlers': local_settings.LOGGING_HANDLER,
			'propagate': True,
			'level': 'DEBUG' if DEBUG else 'INFO',
		},
		'pycountry.db': {
			'handlers': ['null'],
			'propagate': False,
		},
	},
}

# ======================================================================
# SITE SPECIFIC SECTIONS
# ======================================================================

###########
# SATCHMO #
###########
SHOP_CONF = {
	'DEFAULT_NAVISION_JOB': '050',
	'DEFAULT_NAVISION_JSP': 8900,
	'DEFAULT_NAVISION_ACCOUNT': '50.030',
	'ORDER_FILE_PREFX': "hb",
	'ARCHIVE_DEFAULTS': {
		'djangoplicity.products.models.PostCard': { 'ACCOUNT': '50.050', },
		'djangoplicity.products.models.Merchandise': { 'ACCOUNT': '50.050', },
		'djangoplicity.products.models.Media': { 'ACCOUNT': '50.050', },
		'djangoplicity.products.models.Calendar': { 'ACCOUNT': '50.050', },
		'djangoplicity.products.models.ConferenceItem': { 'ACCOUNT': '50.230', },
		'djangoplicity.products.models.Sticker': { 'ACCOUNT': '50.050', },
	}
}


DIRNAME = os.path.abspath( os.path.dirname( __file__ ) )
LOCAL_DEV = True

MIDDLEWARE_CLASSES += (
					"threaded_multihost.middleware.ThreadLocalMiddleware",
					#"satchmo_store.shop.SSLMiddleware.SSLRedirect",
					)

TEMPLATE_CONTEXT_PROCESSORS += ( 'satchmo_store.shop.context_processors.settings', )

AUTHENTICATION_BACKENDS += ( 'satchmo_store.accounts.email-auth.EmailBackend', )

SATCHMO_SETTINGS = {
	'SHOP_BASE': '/shop',
	'MULTISHOP': False,
	'SSL': True,
#	'SHOP_URLS': patterns('',
#		( r'^checkout/', 'spacetelescope.views.shop_closed' ),
#	)
}

SITE_NAME = "Hubbleshop"
SITE_DOMAIN = "www.spacetelescope.org"
LOGDIR = LOG_DIR
LOGFILE = 'satchmo.log'
CHECKOUT_SSL = True

L10N_SETTINGS = {
	'currency_formats': {
		'EURO': {'symbol': u'€', 'positive': u"€ %(val)0.2f", 'negative': u"€ (%(val)0.2f)", 'decimal': ','},
	},
	'default_currency': 'EURO',
	'show_admin_translations': False,
	'allow_translation_choice': False,
}

LIVESETTINGS_OPTIONS = {
	1: {
		'DB': False,
		'SETTINGS': {
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
			u'TAX': {
				u'PRODUCTS_TAXABLE_BY_DEFAULT': u'False',
				u'TAX_SHIPPING': u'False',
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
				u'LIVE_CONFIG_FILE': local_settings.COPOSWEB_CONFIG_INI,
				u'CAPTURE': u'True',
				u'LIVE': u'True' if local_settings.LIVE else u'False',
				u'EXTRA_LOGGING': u'True',
			},
		}
	}
}

ORDER_PREFIX = local_settings.ORDER_PREFIX
LIVE = local_settings.LIVE
SHOP_PICKUP_LOCATIONS = ({
	'id': 'PUP1',
		'name': 'ESO HQ',
		'desc': _( "Self-pickup/ESO HQ in Munich, Germany" ),
		'method': _("Pickup (9-17 CET/CEST) at ESO HQ Reception,"),
		'delivery': _("Karl-Schwarzschild-Str. 2, 85748 Garching, GERMANY"),
	},
)

RECAPTCHA_PUBLIC_KEY = '6LfXJOkSAAAAAE1-HoZR7_iA6D2tT0hGspsqG5mW'
RECAPTCHA_PRIVATE_KEY = '6LfXJOkSAAAAAMETeG2zL8idVr9tW3F0Ndb12GK3'

#
# Pipeline configuration (CSS/JS packing)
#

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# We split the CSS into main and extras to load the more important first
# and the rest in the end. This also solves a problem with IE9 which stops
# loading CSS rules if there are "too many"
PIPELINE_CSS = {
	'main': {
		'source_filenames': (
			'font-awesome/css/font-awesome.min.css',
			'sprites/sprites.css',
			'css/hubble.css',
		),
		'output_filename': 'css/main.css',
	},
	'extras': {
		'source_filenames': (
			'jquery-ui-1.11.1/jquery-ui.min.css',
			'slick-1.5.0/slick/slick.css',
			'justified-gallery/css/justifiedGallery.min.css',
			'magnific-popup/magnific-popup.css',
		),
		'output_filename': 'css/extras.css',
	},
}

PIPELINE_JS = {
	'main': {
		'source_filenames': (
			'jquery/jquery-1.11.1.min.js',
			'jquery-ui-1.11.1/jquery-ui.min.js',
			'bootstrap/bootstrap-3.1.1-dist/js/bootstrap.min.js',
			'js/jquery.menu-aim.js',
			'slick-1.5.0/slick/slick.min.js',
			'djangoplicity/jwplayer/jwplayer.js',
			'djangoplicity/js/jquery.beforeafter-1.4.js',
			'djangoplicity/zoomify/js/ZoomifyImageViewerExpress-min.js',
			'js/masonry.pkgd.min.js',
			'justified-gallery/js/jquery.justifiedGallery.min.js',
			'magnific-popup/jquery.magnific-popup.min.js',
			'djangoplicity/js/widgets.js',
			'djangoplicity/js/pages.js',
			'djangoplicity/js/djp-jwplayer.js',
			'js/picturefill.min.js',
			'js/enquire/enquire.min.js',
			'js/hubble.js',
		),
		'output_filename': 'js/main.js',
	},
	'ie8compat': {
		'source_filenames': (
			'js/ie8compat/matchMedia/matchMedia.js',
			'js/ie8compat/matchMedia/matchMedia.addListener.js',
		),
		'output_filename': 'js/ie8compat.js',
	},
}
PIPELINE_CSS_COMPRESSOR = False
PIPELINE_JS_COMPRESSOR = False
PIPELINE_DISABLE_WRAPPER = True

# IE8 doesn't support application/javascript so we override the default:
PIPELINE_MIMETYPES = (
	(b'text/coffeescript', '.coffee'),
	(b'text/less', '.less'),
	(b'text/javascript', '.js'),
	(b'text/x-sass', '.sass'),
	(b'text/x-scss', '.scss')
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'pipeline.finders.PipelineFinder',
)

# Required since Django 1.5:
ALLOWED_HOSTS = ['.spacetelescope.org', '.eso.org']

# Required since Django 1.6:
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

from djangoplicity.contentserver import CDN77ContentServer
MEDIA_CONTENT_SERVERS = {
	'CDN77': CDN77ContentServer(
		name='CDN77',
		formats={
			'djangoplicity.media.models.images.Image': (
				'large',
				'publicationjpg',
				'screen',
				'wallpaper1',
				'wallpaper2',
				'wallpaper3',
				'wallpaper4',
				'wallpaper5',
				'thumb300y',
				'thumb350x',
				'newsfeature',
				'news',
				'banner1920',
				'screen640',
				'zoomable',
			),
			'djangoplicity.media.models.videos.Video': (
				'videoframe',
				'dome_2kmaster',
				'small_flash',
				'medium_podcast',
				'medium_mpeg1',
				'medium_flash',
				'large_qt',
				'broadcast_sd',
				'hd_and_apple',
				'hd_broadcast_720p50',
				'hd_1080p25_screen',
				'hd_1080p25_broadcast',
				'ultra_hd',
				'ultra_hd_h265',
				'ultra_hd_broadcast',
				'dome_8kmaster',
				'dome_4kmaster',
				'dome_2kmaster',
				'dome_mov',
				'dome_preview',
			),
		},
		url='http://cdn.spacetelescope.org/',
		url_bigfiles='http://cdn2.spacetelescope.org/',
		remote_dir='/www/',
		host='push-19.cdn77.com',
		username='user_v220pif3',
		password='5nkOk3mgr8MDw2d4SZw3',
		api_login='lars@eso.org',
		api_password='054FBaC792mdXA3QkpngOhvWcRqGZJV1',
		cdn_id='33541',
		cdn_id_bigfiles='31465',
	),
}

MEDIA_CONTENT_SERVERS_CHOICES = (
	('', 'Default'),
	('CDN77', 'CDN77'),
)

DEFAULT_MEDIA_CONTENT_SERVER = 'CDN77'

YOUTUBE_TOKEN = '%s/youtube_oauth2_token.json' % TMP_DIR
YOUTUBE_DEFAULT_TAGS = ['Hubble', 'Hubble Space Telecope', 'Telescope', 'Space', 'Observatory', 'ESA']
