# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

# Following variables will be available:
# - PY_VERSION, e.g. "2.7"

import sys

#
# Requirements
#
requirements_repo = "http://www.djangoplicity.org/repository/packages/"
requirements_files = [{'file':'projects/spacetelescope.org/requirements.txt', 'repository':requirements_repo, 'options':['--no-index']}]

# Extra requirements for Python 2.5
if sys.version_info[0] == 2 and sys.version_info[1] < 6:
	requirements_files.append( {'file':'projects/spacetelescope.org/requirements-2.5.txt', 'repository':requirements_repo, 'options':['--no-index']} )

#
# Settings
#
projects_settings = {
	'vcs_projects' : [
			( 'djangoplicity-bootstrap', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-bootstrap',),
			( 'djangoplicity-settings', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-settings' ),
			( 'djangoplicity-adminhistory', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-adminhistory' ),
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
		],
	'develop-symlinks' : [
			( '../../djangoplicity/static', 'projects/spacetelescope.org/static/djangoplicity' ), 
		],
	'requirements' : requirements_files,
	'prompt' : 'spacetelescope.org',
}
settings.update( projects_settings )  
