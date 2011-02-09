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
from bootstrap_settings import settings

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
LOCALROOT = '/Volumes/webdocs'
REMOTEROOT = '/home/web/A'
WEBHOME = '/home/web'

PREFIXI = '%s/%s' % (WEBHOME, SERVERNAMEI)
PREFIX = '%s/%s' % (WEBHOME, SERVERNAME)
PRJDIR = 'projects/%s' % DOMAIN
PRJAPP = 'spacetelescope'
DJANGOPLICITYDIR = 'projects/djangoplicity'

MERGE_FILES = [
	( 'docs', True ),
	( 'docs_maintenance', False ),
	( 'projects/eso_templates', True ),
	( 'tmp/Trash', True ),
	( 'virtualenv/etc/coposweb.ini', False ), 
	( 'logs', False ),
	# NOT COMPLETE - COPOSWEB FILES AND ORDER FILE NEEDED.
]

PERMISSIONS = [
		{'path' : '%(prefix)s/virtualenv/bin/*', 'user' : None, 'group' : None, 'perms' : 'a+x' },
		{'path' : '%(prefix)s/docs/static/css/', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws' },
		{'path' : '%(prefix)s/docs/static/js/', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws' },
		{'path' : '%(prefix)s/logs/', 'user' : None, 'group' : 'w3hst', 'perms' : 'g+ws' },
]

STATIC_FILES = [
	('%(prefix)s/projects/spacetelescope.org/static/','%(prefix)s/docs/static/'),
	('%(prefix)s/projects/djangoplicity/static/','%(prefix)s/docs/static/djangoplicity/'),
]

# Local tasks
local_backupdb = djangoplicity.fabric.backup_database( project_app=PRJAPP )
local_apply_sql = djangoplicity.fabric.apply_sql( sqlfile='sql/deploy.sql', project_app=PRJAPP )

# Integration deployment tasks
integration_clear_installation = djangoplicity.fabric.clear_installation( servers=[DEVSERVER,], prefix=PREFIXI )
integration_bootstrap = djangoplicity.fabric.bootstrap( servers=[DEVSERVER,], prefix=PREFIXI, local_settings='integration_settings' )
integration_relocate_virtualenv = djangoplicity.fabric.relocate_virtualenv( servers=[DEVSERVER,], prefix=PREFIXI, relocateto=PREFIX )
integration_sync = djangoplicity.fabric.sync( servers=[DEVSERVER,], prefix=PREFIXI, sync=STATIC_FILES )
integration_fix_perms = djangoplicity.fabric.fix_perms( servers=[SERVER1I], prefix=PREFIX, dirs=PERMISSIONS )

integration_setup = djangoplicity.fabric.setup( servers=[DEVSERVER,], prefix=PREFIXI, mode='integration' )

integration_vcs_update = djangoplicity.fabric.vcs_update( servers=[DEVSERVER,], prefix=PREFIXI )
integration = djangoplicity.fabric.deploy( servers=[DEVSERVER,], prefix=PREFIXI, prjdir=PRJDIR )
integration_stop = djangoplicity.fabric.stop( servers=[SERVER1I, SERVER2I], servername=SERVERNAME )
integration_start = djangoplicity.fabric.start( servers=[SERVER1I, SERVER2I], servername=SERVERNAME )
integration_stop_static = djangoplicity.fabric.stop_static( servers=[SERVER1I, SERVER2I], servername=SERVERNAME )
integration_start_static = djangoplicity.fabric.start_static( servers=[SERVER1I, SERVER2I], servername=SERVERNAME )
integration_stop_cron = djangoplicity.fabric.stop_cron( servers=[BACKENDDEVSERVER,], prefix=PREFIX, prjdir=PRJDIR, servername=SERVERNAME )
integration_start_cron = djangoplicity.fabric.start_cron( servers=[BACKENDDEVSERVER,], prefix=PREFIX, prjdir=PRJDIR, servername=SERVERNAME )
integration_appsregister = djangoplicity.fabric.appsregister( servers=[BACKENDDEVSERVER,], prefix=PREFIX, prjdir=PRJDIR )
integration_static_deploy = djangoplicity.fabric.static_deploy( servers=[DEVSERVER,], prefix=PREFIXI, prjdir=PRJDIR, staticdir='static' )
integration_locale_deploy = djangoplicity.fabric.locale_deploy( servers=[DEVSERVER,], prefix=PREFIXI, dirs = [ PRJDIR, DJANGOPLICITYDIR ] )
integration_backupdb = djangoplicity.fabric.backup_database( 'conf/settings-integration.ini' )
integration_apply_sql = djangoplicity.fabric.apply_sql( sqlfile='sql/deploy.sql', to_settings='conf/settings-integration.ini' )
integration_setup_online = djangoplicity.fabric.setup_online(
		cronserver = BACKENDDEVSERVER,
		local_root = LOCALROOT,
		remote_root = REMOTEROOT,
		web_home = WEBHOME,
		prefix = PREFIX,
		prefix_env = PREFIXI,
		prjdir = PRJDIR,
		servername = SERVERNAME,
		serverenv = SERVERNAMEI,
		server1 = SERVER1I,
		server2 = SERVER2I,
		devserver = DEVSERVER,
		env = 'integration',
		merge_files = MERGE_FILES,
	)

# Production deployment tasks
production_clear_installation = djangoplicity.fabric.clear_installation( servers=[DEVSERVER,], prefix=PREFIX )
production_relocate_virtualenv = djangoplicity.fabric.relocate_virtualenv( servers=[DEVSERVER,], prefix=PREFIX, relocateto=PREFIX )
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
production_locale_deploy = djangoplicity.fabric.locale_deploy( servers=[DEVSERVER,], prefix=PREFIX, dirs = [ PRJDIR, DJANGOPLICITYDIR ] )
production_backupdb = djangoplicity.fabric.backup_database( 'conf/settings-production.ini' )
production_apply_sql = djangoplicity.fabric.apply_sql( sqlfile='sql/deploy.sql', to_settings='conf/settings-production.ini' )
production_setup_online = djangoplicity.fabric.setup_online(
		cronserver = BACKENDSERVER,
		local_root = LOCALROOT,
		remote_root = REMOTEROOT,
		web_home = WEBHOME,
		prefix = PREFIX,
		prefix_env = PREFIX,
		prjdir = PRJDIR,
		servername = SERVERNAME,
		serverenv = SERVERNAME,
		server1 = SERVER1,
		server2 = SERVER2,
		devserver = DEVSERVER,
		env = 'production',
		merge_files = MERGE_FILES,
	)

# Documentation related tasks
publish_docs = djangoplicity.fabric.publish_docs( domain=DOMAIN )
make_docs = djangoplicity.fabric.make_docs()

# Locale related tasks
makemessages_new = djangoplicity.fabric.makemessages_new( dirs = [ DOMAIN, 'djangoplicity'], languages = ['de-at','nl-be','fr-be','de-be','cs','da','fi','fr','de','is','it','nl','no','pt','pl','es','es-cl','sv','de-ch','fr-ch','it-ch','tr','is'] )
makemessages = djangoplicity.fabric.makemessages( dirs = [ DOMAIN, 'djangoplicity'] )
compilemessages = djangoplicity.fabric.compilemessages( dirs = [ DOMAIN, 'djangoplicity'] )
updatemessages = djangoplicity.fabric.updatemessages( file = '/Users/lnielsen/Desktop/ESON\ Djangoplicity\ Translations\ Strings.csv', languages = [('de-at','Austria'), ('nl-be','Belgium-nl'), ('fr-be','Belgium-fr'), ('de-be','Belgium-de'), ('cs','Czech Republic'), ('da','Denmark'), ('fi','Finland'), ('fr','France'), ('de','Germany'), ('is','Iceland'), ('it','Italy'), ('nl','The Netherlands'), ('no','Norway'), ('pt','Portugal'), ('pl','Poland'), ('es','Spain'), ('es-cl','Chile'), ('sv','Sweden'), ('de-ch','Switzerland-de'), ('fr-ch','Switzerland-fr'), ('it-ch','Switzerland-it'), ('tr','Turkey'), ('is','Iceland'), ] )

# Database related tasks
copydb_production_to_local = djangoplicity.fabric.copy_database( 'conf/settings-production.ini', project_app=PRJAPP )
copydb_integration_to_local = djangoplicity.fabric.copy_database( 'conf/settings-integration.ini', project_app=PRJAPP )
copydb_production_to_integration = djangoplicity.fabric.copy_database( 'conf/settings-production.ini', to_settings='conf/settings-integration.ini' )

# =============== SITE SPECIFIC TASKS BELOW HERE ===============
