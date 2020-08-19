from .dev import *

# just in testing
CELERY_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_RESULT_BACKEND = 'db+sqlite:///results.db'
CELERY_BROKER_URL = 'memory://localhost//'
