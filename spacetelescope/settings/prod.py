from .common import *
from .partials.util import get_secret
import copy
import dj_database_url

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
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE]'

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
