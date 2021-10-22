import copy

from .common import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': SHORT_NAME,
        'LOCATION': [
            '',
            '',
        ],
        'TIMEOUT': 86400
    }
}

DATABASES = copy.deepcopy(DATABASES)
DATABASES['default']['HOST'] = ""
DATABASES['default']['PASSWORD'] = ""

EMAIL_HOST = ''
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE]'

ARCHIVE_AUTO_RESOURCE_DELETION = True

# Shop:
LIVESETTINGS_OPTIONS = copy.deepcopy(LIVESETTINGS_OPTIONS)
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['PSPID'] = u''
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['LIVE'] = u'True'
LIVE = 'True'
ORDER_PREFIX = "hb"

CELERY_BROKER_URL = ''

SOCIAL_FACEBOOK_TOKEN = ""
SOCIAL_TWITTER_TUPLE = (
    "",
    "",
    "",
    "",
)

YOUTUBE_CLIENT_SECRET = '%s/etc/youtube_client_secret_prod.json' % PRJBASE
