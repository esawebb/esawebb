from spacetelescope.settings import *

SITE_ENVIRONMENT = 'production'


DATABASES['default']['HOST'] = "hqdb1.hq.eso.org"
DATABASES['default']['PASSWORD'] = "letoveumtold"


EMAIL_HOST = 'smtphost.hq.eso.org'
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE]'

ARCHIVE_AUTO_RESOURCE_DELETION = True


# Shop:
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['PSPID'] = u'40F06654'
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['LIVE'] = u'True'
LIVE = 'True'
ORDER_PREFIX = "hb"


SOCIAL_FACEBOOK_TOKEN = "144508505618279|5ff52306023505ab445993a2.1-1210975348|12383118425|U_oKxUW-oTKzWHksV5b7I5YCry8"
SOCIAL_TWITTER_TUPLE = (
    "138725262-pvMvidxE9nB3JYlLkR7aBExaSUkm9TFlzawX8wq7",
    "bClNsjLM33fXqtseS0NeXCMwnsggeS9Gi2z3kGl0c",
    "elGtKvRIq8qVCihslKWRQ",
    "syd83XYDRGEDwr0LaZufxs7t7h766L9UM0foxkH0",
)

YOUTUBE_CLIENT_SECRET = '%s/etc/youtube_client_secret_prod.json' % PRJBASE
