import copy

from spacetelescope.settings import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': SHORT_NAME,
        'LOCATION': [
            'aweb48.hq.eso.org:11211',
            'aweb49.hq.eso.org:11211',
        ],
        'TIMEOUT': 86400
    }
}

DATABASES = copy.deepcopy(DATABASES)
DATABASES['default']['HOST'] = "hqdb1.hq.eso.org"
DATABASES['default']['PASSWORD'] = "letoveumtold"

EMAIL_HOST = 'smtphost.hq.eso.org'
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE]'

ARCHIVE_AUTO_RESOURCE_DELETION = True

# Shop:
LIVESETTINGS_OPTIONS = copy.deepcopy(LIVESETTINGS_OPTIONS)
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['PSPID'] = u'40F06654'
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['LIVE'] = u'True'
LIVE = 'True'
ORDER_PREFIX = "hb"

CELERY_BROKER_URL = 'amqp://hubble:letoveumtold@aweb5.hq.eso.org:5672/hubble'

SOCIAL_FACEBOOK_TOKEN = "144508505618279|5ff52306023505ab445993a2.1-1210975348|12383118425|U_oKxUW-oTKzWHksV5b7I5YCry8"
SOCIAL_TWITTER_TUPLE = (
    "138725262-pvMvidxE9nB3JYlLkR7aBExaSUkm9TFlzawX8wq7",
    "bClNsjLM33fXqtseS0NeXCMwnsggeS9Gi2z3kGl0c",
    "elGtKvRIq8qVCihslKWRQ",
    "syd83XYDRGEDwr0LaZufxs7t7h766L9UM0foxkH0",
)

YOUTUBE_CLIENT_SECRET = '%s/etc/youtube_client_secret_prod.json' % PRJBASE
