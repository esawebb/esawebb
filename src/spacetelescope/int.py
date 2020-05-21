import copy

from spacetelescope.settings import *

DATABASES = copy.deepcopy(DATABASES)
DATABASES['default']['HOST'] = ""
DATABASES['default']['PASSWORD'] = ""


EMAIL_HOST = 'smtphost.hq.eso.org'
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE-INTEGRATION]'


CELERY_BROKER_URL = ''


# Shop:
ORDER_PREFIX = "hbi"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': 'nova',
        'LOCATION': [
            '',
        ],
        'TIMEOUT': 86400
    },
}
