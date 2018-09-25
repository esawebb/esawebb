# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2014 ESO & ESA/Hubble
#
# Authors:
#   Mathias Andre <mandre@eso.org>

from __future__ import absolute_import

from celery import Celery

from django.conf import settings

app = Celery('spacetelescope')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print 'Request: {0!r}'.format(self.request)
