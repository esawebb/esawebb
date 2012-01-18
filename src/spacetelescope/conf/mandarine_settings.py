# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from default_settings import *
from djangoplicity.settings import copy_setting

ADMINS = (
	('Luis Clara Gomes','lcgomes@eso.org'),
)

LOGGING_HANDLER = ['console']

##############
# DEPLOYMENT #
##############
DEPLOYMENT_EXISTING_CHECKOUT = "~/Workspaces/web/"

##########	
# CELERY #
##########
BROKER_HOST = "localhost"
#BROKER_HOST = "aweb26.hq.eso.org"
CELERY_ALWAYS_EAGER = True

########
# LDAP #
########
DISABLE_LDAP = True