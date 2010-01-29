# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
from fabric.api import *
import djangoplicity.fabric


SERVERNAME = "hubble"
SERVERNAMEI = "hubblei"
DOMAIN = "spacetelescope.org"
SERVER1I = "hubble1i"
SERVER2I = "hubble2i"
SERVER1 = "hubble1"
SERVER2 = "hubble2"
DEVSERVER = "aweb8"
BACKENDDEVSERVER = "aweb9"
BACKENDSERVER = "aweb10"

PREFIXI = '/home/web/%s' % SERVERNAMEI
PREFIX = '/home/web/%s' % SERVERNAME
PRJDIR = 'projects/%s' % DOMAIN

integration_clear_installation = djangoplicity.fabric.clear_installation( servers=[DEVSERVER,], prefix=PREFIXI )
integration_relocate_virtualenv = djangoplicity.fabric.relocate_virtualenv( servers=[DEVSERVER,], prefix=PREFIXI, relocateto='/home/web/hubble' )
integration_setup = djangoplicity.fabric.setup( servers=[DEVSERVER,], prefix=PREFIXI, mode='integration' )
integration_fix_perms = djangoplicity.fabric.fix_perms( servers=[SERVER1I], prefix=PREFIX )
integration = djangoplicity.fabric.deploy( servers=[DEVSERVER,], prefix=PREFIXI, prjdir=PRJDIR )
integration_stop = djangoplicity.fabric.stop( servers=[SERVER1I, SERVER2I], servername=SERVERNAME )
integration_start = djangoplicity.fabric.start( servers=[SERVER1I, SERVER2I], servername=SERVERNAME )
integration_stop_static = djangoplicity.fabric.stop_static( servers=[SERVER1I, SERVER2I], servername=SERVERNAME )
integration_start_static = djangoplicity.fabric.start_static( servers=[SERVER1I, SERVER2I], servername=SERVERNAME )
integration_stop_cron = djangoplicity.fabric.stop_cron( servers=[BACKENDDEVSERVER,], prefix=PREFIX, prjdir=PRJDIR, servername=SERVERNAME )
integration_start_cron = djangoplicity.fabric.start_cron( servers=[BACKENDDEVSERVER,], prefix=PREFIX, prjdir=PRJDIR, servername=SERVERNAME )
integration_appsregister = djangoplicity.fabric.appsregister( servers=[BACKENDDEVSERVER,], prefix=PREFIX, prjdir=PRJDIR )
integration_static_deploy = djangoplicity.fabric.static_deploy( servers=[DEVSERVER,], prefix=PREFIXI, prjdir=PRJDIR, staticdir='static' )

production_clear_installation = djangoplicity.fabric.clear_installation( servers=[DEVSERVER,], prefix=PREFIX )
production_relocate_virtualenv = djangoplicity.fabric.relocate_virtualenv( servers=[DEVSERVER,], prefix=PREFIX, relocateto='/home/web/hubble' )
production_setup = djangoplicity.fabric.setup( servers=[DEVSERVER,], prefix=PREFIX, mode='production' )
production = djangoplicity.fabric.deploy( servers=[DEVSERVER,], prefix=PREFIX, prjdir=PRJDIR )
production_stop = djangoplicity.fabric.stop( servers=[SERVER1, SERVER2], servername=SERVERNAME )
production_start = djangoplicity.fabric.start( servers=[SERVER1, SERVER2], servername=SERVERNAME )
production_stop_static = djangoplicity.fabric.stop_static( servers=[SERVER1, SERVER2], servername=SERVERNAME )
production_start_static = djangoplicity.fabric.start_static( servers=[SERVER1, SERVER2], servername=SERVERNAME )
production_stop_cron = djangoplicity.fabric.stop_cron( servers=[BACKENDSERVER,], prefix=PREFIX, prjdir=PRJDIR, servername=SERVERNAME )
production_start_cron = djangoplicity.fabric.start_cron( servers=[BACKENDSERVER,], prefix=PREFIX, prjdir=PRJDIR, servername=SERVERNAME )
production_appsregister = djangoplicity.fabric.appsregister( servers=[BACKENDSERVER,], prefix=PREFIX, prjdir=PRJDIR )
production_static_deploy = djangoplicity.fabric.static_deploy( servers=[DEVSERVER,], prefix=PREFIX, prjdir=PRJDIR, staticdir='static' )

# =============== SITE SPECIFIC TASKS BELOW HERE ===============
