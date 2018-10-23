import copy

from spacetelescope.settings import *

DATABASES = copy.deepcopy(DATABASES)
DATABASES['default']['HOST'] = "hqdb1i.hq.eso.org"
DATABASES['default']['PASSWORD'] = "fivjeylvoked"


EMAIL_HOST = 'smtphost.hq.eso.org'
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE-INTEGRATION]'


CELERY_BROKER_URL = 'amqp://spacetelescope:letoveumtold@aweb36.hq.eso.org:5672/spacetelescope_vhost'


# Shop:
ORDER_PREFIX = "hbi"
