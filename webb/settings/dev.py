import sys
from .common import *
from .partials.util import get_secret
import copy
import dj_database_url

SECRET_KEY = get_secret('DJANGO_SECRET_KEY')
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SECURE_PROXY_SSL_HEADER = None

ALLOWED_HOSTS = ['*']


def show_toolbar(request):
    '''
    The default callback checks if the IP is internal, but docker's IP
    addresses are not in INTERNAL_IPS, so we force the display in dev mode
    '''
    return True


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    'SKIP_TEMPLATE_PREFIXES': (
        'django/forms/widgets/',
        'admin/widgets/',
        'menus/',
        'pipeline/',
    ),
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
#   'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
#   'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

##################
# DATABASE SETUP #
##################
if get_secret('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config()
    }

##########
# CACHE  #
##########
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': SHORT_NAME,
        'LOCATION': [
            'cache:11211',
        ],
        'TIMEOUT': 86400
    }
}



##########
# CELERY #
##########
CELERY_BROKER_URL = 'amqp://{}:{}@broker:5672/'.format(get_secret('RABBITMQ_USER'), get_secret('RABBITMQ_PASS'))

# Avoid infinite wait times and retries
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

ARCHIVE_AUTO_RESOURCE_DELETION = True

SERVE_STATIC_MEDIA = True

#########
# EMAIL #
#########
EMAIL_SUBJECT_PREFIX = '[ESA/WEBB]'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = get_secret('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_PASSWORD')
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

##################
# CATPCHA #
##################
# This keys are provided by google for testing purposes
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

##################
# CONTENT SERVER #
##################
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
                'news',
            ),
        },
        url='https://cdn3.esawebb.org/',
        url_bigfiles='https://cdn4.esawebb.org/',
        remote_dir='/www/',
        host='push-12.cdn77.com',
        username=get_secret('CDN_STORAGE_USERNAME'),
        password=get_secret('CDN_STORAGE_PASSWORD'),
        api_login=get_secret('CDN_API_LOGIN'),
        api_password=get_secret('CDN_API_PASSWORD'),
        apiv3_token=get_secret('CDN_API_TOKEN'),
        cdn_id='1047011652',
        cdnv3_id='1047011652',
        cdn_id_bigfiles='1653546147',
        cdnv3_id_bigfiles='1653546147',
    ),
}

MEDIA_CONTENT_SERVERS_CHOICES = (
    ('', 'Default'),
    ('CDN77', 'CDN77'),
)

DEFAULT_MEDIA_CONTENT_SERVER = 'CDN77'
