# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

import sys

#
# Make sure the settings can be loaded in other modules (currently fabfile.py, deploy.py and bootstrap.py)
# 
if 'settings' not in globals():
	from djangoplicity.bootstrap.defaults import settings, PY_VERSION, run_function, task_move, task_append, task_run_manage
	 
	
#
# Requirements
#
requirements_repo = "http://www.djangoplicity.org/repository/packages/"
requirements_files = [{'file':'projects/spacetelescope.org/requirements.txt', 'repository':requirements_repo, 'options':['--no-index']}]

if sys.version_info[0] == 2 and sys.version_info[1] == 5:
	requirements_files.append( {'file':'projects/spacetelescope.org/requirements-2.5.txt', 'repository':requirements_repo, 'options':['--no-index']} )
	
#
# Settings
#
projects_settings = {
	'vcs_projects' : [
			( 'djangoplicity-bootstrap', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-bootstrap',),
			( 'djangoplicity-settings', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-settings' ),
			( 'djangoplicity-adminhistory', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-adminhistory' ),
			( 'djangoplicity-fabric', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-fabric',),
			( 'djangoplicity-social', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-social',),
			( 'djangoplicity', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity' ),
			( 'spacetelescope.org', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/spacetelescope.org' ), 
		],	
	'directories' : settings['directories'] + [
			'docs',
            'docs/static',
            'docs/static/djangoplicity',
            'docs/static/archives',
            'docs/static/archives/images/',
			'docs/static/archives/videos/',
			'docs/static/archives/releases/',
		],
	'symlinks' : [
			( '../../virtualenv/lib/python%(version)s/site-packages/django/contrib/admin/media' % { 'version' : PY_VERSION }, 'docs/static/media' ),
			( '../import' % { 'version' : PY_VERSION }, 'import' ), 
		],
	'develop-symlinks' : [
			( '../../djangoplicity/static', 'projects/spacetelescope.org/static/djangoplicity' ), 
		],
	'requirements' : requirements_files,
	'prompt' : 'spacetelescope.org',
	'manage.py' : 'projects/spacetelescope.org/src/spacetelescope/manage.py',
	'settings_module' : 'spacetelescope.settings',
	'finalize_tasks' : [ 
		run_function( task_run_manage, task='config_gen' ), 
		run_function( task_append, src='tmp/conf/activate-djangoplicity.sh', dst='virtualenv/bin/activate', marker="DJANGOPLICITY" ),
		run_function( task_append, src='tmp/conf/activate-djangoplicity.csh', dst='virtualenv/bin/activate.csh', marker="DJANGOPLICITY" ), 
		run_function( task_move, src='tmp/conf/httpd-djangoplicity.conf', dst='virtualenv/apache/'),
		run_function( task_move, src='tmp/conf/django.wsgi', dst='virtualenv/apache/django.wsgi' ),
	]
}
settings.update( projects_settings )
