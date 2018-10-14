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
import os
import re

# pylint: disable=no-name-in-module
from celery.schedules import crontab

# We can't use ugettext from django.utils.translation as it will itself
# load the settings resulting in a ImproperlyConfigured error
ugettext = lambda s: s


import djangoplicity.crosslinks
from djangoplicity.contentserver import CDN77ContentServer

#############################
# ENVIRONMENT CONFIGURATION #
#############################
SHORT_NAME = 'hubble'
ROOT = '/app'
ARCHIVE_IMPORT_ROOT = '%s/import' % ROOT
PRJBASE = "%s/src/spacetelescope" % ROOT
PRJNAME = 'spacetelescope.org'
DJANGOPLICITY_ROOT = "%s/src/djangoplicity" % ROOT
LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
GA_ID = "UA-2368492-6"
FACEBOOK_APP_ID = "144508505618279"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


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

SITE_ENVIRONMENT = os.getenv('ENVIRONMENT')
DEBUG = SITE_ENVIRONMENT == 'dev'
DEBUG_TOOLBAR = DEBUG
DEBUG_TOOLBAR_CONFIG = {}
DEBUG_TOOLBAR_PANELS = []

ADMINS = (
    ('EPO Monitoring', 'esoepo-monitoring@eso.org'),
)
MANAGERS = ADMINS

SERVE_STATIC_MEDIA = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"


##################
# DATABASE SETUP #
##################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spacetelescope',
        'USER': 'spacetelescope',
        'PASSWORD': '',
        'HOST': 'localhost',
        'CONN_MAX_AGE': 600,
    }
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

LANGUAGES = (
    ( 'en', ugettext( 'English' ) ),
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
DATE_FORMAT = ugettext('j F Y')
DATE_LONG_FORMAT = ugettext('j F Y')
DATETIME_FORMAT = ugettext('M j, Y, H:i T')
DATETIME_LONG_FORMAT = ugettext('M j, Y y, H:i T')
MONTH_DAY_FORMAT = ugettext('F j')
TIME_FORMAT = ugettext('H:i T')
YEAR_MONTH_FORMAT = ugettext('F Y')
WIDGET_FORMAT = ugettext("j/m/Y")

###############
# MEDIA SETUP #
###############
MEDIA_ROOT = "%s/docs/static/" % ROOT
MEDIA_URL = "/static/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# ADMIN_MEDIA_PREFIX is necessary due to satchmo current version. TODO: remove when Satchmo is upgraded
ADMIN_MEDIA_PREFIX = "/static/app/admin/"
DJANGOPLICITY_MEDIA_URL = "/static/app/djangoplicity/"
DJANGOPLICITY_MEDIA_ROOT = "%s/static" % DJANGOPLICITY_ROOT

MIDENTIFY_PATH = '/usr/bin/midentify'

# Staticfiles app
STATICFILES_DIRS = [
    ( 'djangoplicity', DJANGOPLICITY_MEDIA_ROOT ),
]

STATIC_ROOT = "%s/static/djp/" % ROOT
STATIC_URL = "/static/djp/"

##########
# CACHE  #
##########
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': SHORT_NAME,
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 86400
    }
}
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = SHORT_NAME
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# keyedcached settings:
CACHE_TIMEOUT = CACHE_MIDDLEWARE_SECONDS if CACHES['default']['BACKEND'] != 'django.core.cache.backends.dummy.DummyCache' else 0  # prevents stupid error from keyecache
KEY_PREFIX = SHORT_NAME

USE_ETAGS = True

#############
# TEMPLATES #
#############
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PRJBASE + '/templates',
            DJANGOPLICITY_ROOT + '/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'djangoplicity.utils.context_processors.project_environment',
                'djangoplicity.utils.context_processors.google_analytics_id',
                'djangoplicity.utils.context_processors.djangoplicity_environment',
                'djangoplicity.archives.context_processors.internal_request',
                'satchmo_store.shop.context_processors.settings',
            ],
        },
    },
]

ROOT_URLCONF = 'spacetelescope.urls'

###############################
# MIDDLEWARE AND APPLICATIONS #
###############################
MIDDLEWARE = (
    # Compresses content for browsers that understand gzip compression (all modern browsers).
    'django.middleware.gzip.GZipMiddleware',  # Response

    # Handles conditional GET operations. If the response has a ETag or Last-Modified header,
    # and the request has If-None-Match or If-Modified-Since, the response is replaced by an
    # HttpNotModified.
    'django.middleware.http.ConditionalGetMiddleware',

    # The CsrfMiddleware class provides easy-to-use protection against Cross Site Request Forgeries.
    'django.middleware.csrf.CsrfViewMiddleware',
)

if DEBUG_TOOLBAR:
    # Add debug toolbar to request
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )


MIDDLEWARE += (
    # Enables session support
    'django.contrib.sessions.middleware.SessionMiddleware',  # Request/Response (db)

    # Adds the user attribute, representing the currently-logged-in user, to every incoming
    # HttpRequest object.
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Request

    # enables Messaging middleware
    'django.contrib.messages.middleware.MessageMiddleware',

)

if USE_I18N:
    MIDDLEWARE += (
        # Sets local for request based on URL prefix.
        'djangoplicity.translation.middleware.LocaleMiddleware',  # Request/Response
    )

MIDDLEWARE += (
    # - Forbids access to user agents in the DISALLOWED_USER_AGENTS setting
    # - Performs URL rewriting based on the APPEND_SLASH and PREPEND_WWW settings.
    # - Handles ETags based on the USE_ETAGS setting.
    'django.middleware.common.CommonMiddleware',  # Request/Response


    # Sets a boolean session variable INTERNAL_REQUEST if request.META['REMOTE_ADDR'] is in INTERNAL_IPS
    'djangoplicity.archives.middleware.InternalRequestMiddleware',  # Request
)


MIDDLEWARE += (
    # Module for URL redirection.
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',  # Response

    # Module for URL redirection based on regular expressions
    'djangoplicity.utils.middleware.RegexRedirectMiddleware',  # Response

    'djangoplicity.archives.contrib.satchmo.middleware.SatchmoSSLRedirectOverride',
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
    'djangoplicity.cutter',
    #'djangoplicity.mailer',
    #'djangoplicity.scrum',
    #'djangoplicity.kiosk.engine',
    #'djangoplicity.kiosk.slides',
    'spacetelescope',
    'spacetelescope.frontpage',
    'mptt',
    'django_extensions',
    'django_mailman',
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
    'djangoplicity.concardis',
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
    'tinymce',
)


if DEBUG_TOOLBAR:
    INSTALLED_APPS += (
        'debug_toolbar',
    )

############
# SESSIONS #
############
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 86400
SESSION_COOKIE_DOMAIN = None


################
# FILE UPLOADS #
################
FILE_UPLOAD_TEMP_DIR = TMP_DIR
FILE_UPLOAD_PERMISSIONS = 0666

SERVER_EMAIL = 'nobody@eso.org'
DEFAULT_FROM_EMAIL = 'nobody@eso.org'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE-LOCAL]'

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
ASSETS_DEBUG = DEBUG
ASSETS_UPDATER = "timestamp"

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
ARCHIVE_ROOT = 'archives/'

ENABLE_ADVANCED_SEARCH = True
ADV_SEARCH_START_YEAR = 1998

ARCHIVE_AUTO_RESOURCE_DELETION = False
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
DEFAULT_CONTACT_CITY = u"Garching bei München"
DEFAULT_CONTACT_STATE_PROVINCE = ""
DEFAULT_CONTACT_POSTAL_CODE = u"D-85748"
DEFAULT_CONTACT_COUNTRY = u"Germany"
DEFAULT_RIGHTS = "Creative Commons Attribution 4.0 International License"
DEFAULT_PUBLISHER = u"ESA/Hubble"
DEFAULT_PUBLISHER_ID = u"esahubble"

DEFAULT_CREDIT = u"NASA &amp; ESA"

MP4BOX_PATH = '/usr/bin/MP4Box'
MP4FRAGMENT_PATH = '/opt/bin/mp4fragment'

ARCHIVE_WORKFLOWS = {
    'media.video.rename': ('spacetelescope.workflows.media', 'video_rename'),
}

VIDEO_RENAME_NOTIFY = ['hzodet@eso.org', 'mkornmes@eso.org']

ARCHIVE_CROSSLINKS = djangoplicity.crosslinks.crosslinks_for_domain('spacetelescope.org')

##########
# SOCIAL #
##########
SOCIAL_FACEBOOK_TOKEN = "187807957898842|a7f1fed4a89e26492133c6e4-100001473653251|141347899254844|K4lqzDRBPyAVFa7msmusumliPwI"
SOCIAL_TWITTER_TUPLE = (
    "226991078-bHYf0sHAUEs1v6fjnxy8F0KjTLtSLnqTpyKx2Bqh",
    "oiRDpzBIZUmQ1m8xxrw16aiYBAMjBx9vEi4ddgLOjzc",
    "uS6hO2sV6tDKIOeVjhnFnQ",
    "MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk",
)


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

CELERY_IMPORTS = [
    "djangoplicity.archives.contrib.security.tasks",
    "djangoplicity.celery.tasks",
]

# Message routing
CELERY_TASK_DEFAULT_QUEUE = "celery"
CELERY_TASK_DEFAULT_EXCHANGE = "celery"
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_TASK_DEFAULT_ROUTING_KEY = "celery"
CELERY_TASK_QUEUES = {
    "celery": {
        "exchange": "celery",
        "exchange_type": "direct",
        "binding_key": "celery",
    },
}

CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False

# Broker settings.
CELERY_BROKER_USE_SSL = False
CELERY_BROKER_URL = 'amqp://spacetelescope:letoveumtold@localhost:5672/spacetelescope_vhost'

# Task result backend
CELERY_RESULT_BACKEND = "amqp"

# AMQP backend settings
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_EXPIRES = 3600

# Task execution
CELERY_TASK_IGNORE_RESULT = True
CELERY_WORKER_DISABLE_RATE_LIMITS = True

# Events
CELERY_WORKER_SEND_TASK_EVENTS = True

# Logging
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

CELERY_TASK_ALWAYS_EAGER = False

# File to save revoked tasks across workers restart
CELERY_WORKER_STATE_DB = "%s/tmp/celery_states" % ROOT
CELERY_BEAT_SCHEDULE_FILENAME = '%s/tmp/celerybeat_schedule' % ROOT

# Define Celery periodic tasks
CELERY_BEAT_SCHEDULE = {
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
    'check-content-server-resources-all': {
        'task': 'djangoplicity.contentserver.tasks.check_content_server_resources',
        'schedule': crontab(minute=0, hour=10, day_of_week='sun'),
        'kwargs': {'last': 15000},  # Large enough to check all resources
    },
    'cdn77-purge-prefetch': {
        'task': 'djangoplicity.contentserver.cdn77_tasks.purge_prefetch',
        'schedule': crontab(minute='*/10'),  # Every 10 minutes
    },
    'shop-subscribers': {
        'task': 'djangoplicity.archives.contrib.satchmo.tasks.shop_subscribers',
        'schedule': crontab(minute=0, hour=9, day_of_week='sun'),
    },
    'clearsessions': {
        'task': 'djangoplicity.celery.tasks.clearsessions',
        'schedule': crontab(minute=0, hour=3),
    },
}

##############
# JavaScript #
##############
JQUERY_JS = "jquery/jquery-1.11.1.min.js"
JQUERY_UI_JS = "jquery-ui-1.12.1/jquery-ui.min.js"
JQUERY_UI_CSS = "jquery-ui-1.12.1/jquery-ui.min.css"
DJANGOPLICITY_ADMIN_CSS = "djangoplicity/css/admin.css"
DJANGOPLICITY_ADMIN_JS = "djangoplicity/js/admin.js"
SUBJECT_CATEGORY_CSS = "djangoplicity/css/widgets.css"

REGEX_REDIRECTS = (
#   ( re.compile( '/hubbleshop/webshop/webshop\.php\?show=sales&section=(books|cdroms)' ), '/shop/category/\g<1>/' ),
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
    'disable_existing_loggers': False,
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
            'class': 'logging.NullHandler',
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
            'handlers': ['console'] if DEBUG else ['file'],
            'propagate': True,
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.template': {
            'handlers': ['null'],
            'propagate': False,
        },
        'djangoplicity': {
            'handlers': ['console'] if DEBUG else ['file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console'] if DEBUG else ['file'],
            'propagate': False,
            'level': 'INFO',
        },
        'sslurllib': {
            'handlers': ['null', ],
            'propagate': False,
        },
        'django_auth_ldap': {
            'handlers': ['console'] if DEBUG else ['file'],
            'propagate': True,
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'pycountry.db': {
            'handlers': ['null'],
            'propagate': False,
        },
        'iterchoices': {
            'handlers': ['null'],
            'propagate': False,
        },
        'tinymce': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['console'] if DEBUG else ['file'],
            'level': 'WARNING',  # requests is too verbose by default
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

MIDDLEWARE += (
    "threaded_multihost.middleware.ThreadLocalMiddleware",
)

AUTHENTICATION_BACKENDS += ( 'satchmo_store.accounts.email-auth.EmailBackend', )

SATCHMO_SETTINGS = {
    'SHOP_BASE': '/shop',
    'MULTISHOP': False,
    'SSL': True,
#   'SHOP_URLS': patterns('',
#       ( r'^checkout/', 'spacetelescope.views.shop_closed' ),
#   )
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
                u'MODULES': u'["PAYMENT_CONCARDIS"]'
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
                u'LOGO_URI': u'http://hubble3.hq.eso.org/static/archives/logos/screen/eso_colour.jpg',  # FIXME This should point to www.spacetelescope.org but is currently broken until the ACE is decomissioned
            },
            u'PAYMENT_CONCARDIS': {
                u'PSPID': u'esoepod',
                u'SHA_IN_PASSPHRASE': u'0;dl18;asdL_k21as87ma',
                u'SHA_OUT_PASSPHRASE': u'!7-zl;j31njky;aslerl',
                u'LIVE': u'False',
                u'EXTRA_LOGGING': u'True',
            },
        }
    }
}

ORDER_PREFIX = 'hbl'
LIVE = False
SHOP_PICKUP_LOCATIONS = ({
    'id': 'PUP1',
    'name': 'ESO HQ',
    'desc': ugettext( "Self-pickup/ESO HQ in Munich, Germany" ),
    'method': ugettext("Pickup (9-17 CET/CEST) at ESO HQ Reception,"),
    'delivery': ugettext("Karl-Schwarzschild-Str. 2, 85748 Garching, GERMANY"),
},)

RECAPTCHA_PUBLIC_KEY = '6LcUjdQSAAAAAHWYDCgHT40vC0NLzUPcmwVDh9yU'
RECAPTCHA_PRIVATE_KEY = '6LcUjdQSAAAAAPHRoDu56rlNylGTtKvHgfJFTGcE'

#
# Pipeline configuration (CSS/JS packing)
#

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# We split the CSS into main and extras to load the more important first
# and the rest in the end. This also solves a problem with IE9 which stops
# loading CSS rules if there are "too many"
PIPELINE = {
    'STYLESHEETS': {
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
                'jquery-ui-1.12.1/jquery-ui.min.css',
                'slick-1.5.0/slick/slick.css',
                'justified/css/jquery.justified.css',
                'magnific-popup/magnific-popup.css',
            ),
            'output_filename': 'css/extras.css',
        },
    },
    'JAVASCRIPT': {
        'main': {
            'source_filenames': (
                'jquery/jquery-1.11.1.min.js',
                'jquery-ui-1.12.1/jquery-ui.min.js',
                'bootstrap/bootstrap-3.1.1-dist/js/bootstrap.min.js',
                'js/jquery.menu-aim.js',
                'slick-1.5.0/slick/slick.min.js',
                'djangoplicity/jwplayer/jwplayer.js',
                'djangoplicity/js/jquery.beforeafter-1.4.js',
                'djangoplicity/zoomify/js/ZoomifyImageViewerExpress-min.js',
                'js/masonry.pkgd.min.js',
                'justified/js/jquery.justified.min.js',
                'magnific-popup/jquery.magnific-popup.min.js',
                'djangoplicity/js/widgets.js',
                'djangoplicity/js/pages.js',
                'djangoplicity/js/djp-jwplayer.js',
                'js/picturefill.min.js',
                'js/enquire/enquire.min.js',
                'js/sorttable.js',
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
    },
    'CSS_COMPRESSOR': False,
    'JS_COMPRESSOR': False,
    'DISABLE_WRAPPER': True,
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# Required since Django 1.5:
ALLOWED_HOSTS = [
    'localhost',
    '.spacetelescope.org',
    '.eso.org',
]

# Required since Django 1.6:
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

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
                'thumb150y',
                'thumb300y',
                'thumb350x',
                'thumb700x',
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
                'cylindrical_4kmaster',
                'cylindrical_8kmaster',
                'cylindrical_16kmaster',
            ),
        },
        url='https://cdn.spacetelescope.org/',
        url_bigfiles='https://cdn2.spacetelescope.org/',
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
YOUTUBE_DEFAULT_TAGS = ['Hubble', 'Hubble Space Telescope', 'Telescope', 'Space', 'Observatory', 'ESA']
YOUTUBE_CLIENT_SECRET = '%s/etc/youtube_client_secret.json' % PRJBASE

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
        textcolor save link image media preview codesample table
        code lists fullscreen  insertdatetime  nonbreaking contextmenu
        directionality searchreplace wordcount visualblocks visualchars
        code fullscreen autolink lists  charmap print  hr anchor pagebreak
    ''',
    'toolbar1': '''
        fullscreen code | cut copy | searchreplace | alignleft aligncenter alignright alignjustify | formatselect forecolor backcolor |superscript subscript |
     ''',
    'toolbar2': '''
        bold italic underline strikethrough | bullist numlist table hr | indent outdent | undo redo | link unlink anchor image media charmap | nonbreaking |
    ''',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'statusbar': True,
    'entity_encoding': 'raw',
    'convert_urls': False,
}

NEWSLETTER_SUBSCRIBERS_URL = 'https://us2.admin.mailchimp.com/lists/members/import/setup?id=518373&type=CutPaste'
