from .common import *
from .partials.util import get_secret
import copy
import dj_database_url


SECRET_KEY = get_secret('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    '.esahubble.org',
    '.spacetelescope.org'
]

# Required to import a big number of images using the admin import form
DATA_UPLOAD_MAX_NUMBER_FIELDS = 200000

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'KEY_PREFIX': SHORT_NAME,
#         'LOCATION': [
#             '',
#             '',
#         ],
#         'TIMEOUT': 86400
#     }
# }

# DATABASE
if get_secret('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config()
    }

EMAIL_HOST = ''
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = '[ESA/HUBBLE]'

ARCHIVE_AUTO_RESOURCE_DELETION = True

# Shop:
LIVESETTINGS_OPTIONS = copy.deepcopy(LIVESETTINGS_OPTIONS)
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['PSPID'] = u''
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['LIVE'] = u'True'
LIVE = 'True'
ORDER_PREFIX = "hb"

# CELERY
CELERY_BROKER_URL = 'amqp://{}:{}@broker:5672/'.format(get_secret('RABBITMQ_USER'), get_secret('RABBITMQ_PASS'))

SOCIAL_FACEBOOK_TOKEN = ""
SOCIAL_TWITTER_TUPLE = (
    "",
    "",
    "",
    "",
)

YOUTUBE_CLIENT_SECRET = '%s/etc/youtube_client_secret_prod.json' % PRJBASE
