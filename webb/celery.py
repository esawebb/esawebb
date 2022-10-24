# -*- coding: utf-8 -*-
#
# webb.org
# Copyright 2014 ESO & ESA/Hubble
#
# Authors:
#   Mathias Andre <mandre@eso.org>

from __future__ import absolute_import
from __future__ import print_function
import sys

from celery import Celery

from django.conf import settings
import os

environment = os.environ.get('ENVIRONMENT', 'dev')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webb.settings.{}".format(environment))

app = Celery('webb')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# A strange bug with Celery makes the first few tasks fail if CONN_MAX_AGE
# is set:
# OperationalError: could not receive data from server: Bad file descriptor
# As a workaround we disable the settings if running in celery
if 'celery' in sys.argv[0]:
    print('Djangoplicity: Disabling CONN_MAX_AGE')
    settings.DATABASES['default']['CONN_MAX_AGE'] = 0


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(bind=True)
def rename_resources_under_cdn(self):
    from datetime import datetime, timedelta
    from djangoplicity.media.models import Video, Image
    remove_id = '-h1dd3n'

    date = datetime.now()
    date_pass = datetime.now() + timedelta(minutes=5)
    staged_images = Image.objects.filter(release_date__gte=date, release_date__lte=date_pass)
    for image in staged_images:
        try:
            new_pk = image.id.replace(remove_id, '')
            image.rename(new_pk)
        except e:
            print(e)