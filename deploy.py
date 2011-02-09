#!/usr/bin/env python
## WARNING: This file is generated
#!/usr/bin/env python
"""Deploy a djangoplicity project


Note this entire process can be greatly simplified if 
PIP is being used to install directly from VCS. However
at the moment, we still need resources local on the disk,
before being installed with PIP, and thus we need this script.

Script is based on the virtualenv script
"""

import sys
import os
import optparse
	
############################################################
## Main

logger = None
call_subprocess = None

def main():
	parser = optparse.OptionParser( usage="%prog [OPTIONS] BASE_DIR" )

	parser.add_option( 
		'-v', '--verbose',
		action = 'count',
		dest = 'verbose',
		default = 0,
		help = "Increase verbosity" )

	parser.add_option( 
		'-q', '--quiet',
		action = 'count',
		dest = 'quiet',
		default = 0,
		help = 'Decrease verbosity' )

	options, args = parser.parse_args()

	if not args:
		print 'You must provide a BASE_DIR'
		parser.print_help()
		sys.exit(2)
	if len(args) > 1:
		print 'There must be only one argument: BASE_DIR (you gave %s)' % (
			' '.join(args))
		parser.print_help()
		sys.exit(2)

	if 'settings' not in globals() or 'VIRTUALENV_DIRNAME' not in globals():
		print 'Invalid script - no settings included in script.'
		sys.exit(3)
	
	base_dir = args[0]
	
	global settings, VIRTUALENV_DIRNAME
	
	# Paths
	home_dir = os.path.join( base_dir, VIRTUALENV_DIRNAME )
	bin_dir = os.path.join( home_dir, 'Scripts' if sys.platform == 'win32' else 'bin' )
	#_activate_virtualenv( bin_dir )
		
	# Logger
	from virtualenv import Logger
	from pip import call_subprocess as pip_call_subprocess
	global call_subprocess
	global logger
	verbosity = options.verbose - options.quiet
	logger = Logger( [( Logger.level_for_integer( 2 - verbosity ), sys.stdout )] )
	call_subprocess = pip_call_subprocess
			
	class options:
		develop = False
		
	
	task_vcs_update( base_dir )
	task_install_requirements( base_dir, home_dir, bin_dir )
	task_vcs_install( base_dir, home_dir, bin_dir, options )

############################################################
## Tasks

def task_vcs_update( base_dir ):
	"""
	Checkout VCS project
	"""
	logger.notify("Running version controls updates")
	
	vcs_base_dir = os.path.join( base_dir, _get_setting( 'vcs_base_dir', 'projects' ) )
	vcs_projects = _get_setting( 'vcs_projects', [] )
	
	if not os.path.exists( vcs_base_dir ):
		logger.error("VCS base directory %s doesn't exists.")
		return
	
	if vcs_projects:
		# Register all version control modules
		from pip import version_control
		version_control()
		from pip.vcs import vcs
		
		# Loop over projects
		for vcs_dirname, vcs_url in vcs_projects:
			vcs_dir = os.path.join( vcs_base_dir, vcs_dirname )
			
			# Update project
			#try:
			vc_type, url = vcs_url.split( '+', 1 )
			backend = vcs.get_backend( vc_type )
			if backend:
				logger.info( "Updating VCS project from URL %s " % vcs_url )
				vcs_backend = backend( vcs_url )
				url, rev = vcs_backend.get_url_rev()
				rev_options = [rev] if rev else []
				vcs_backend.update( vcs_dir, rev_options )
			else:
				logger.error( "Unexpected version control type (in %s): %s" % ( url, vc_type ) )
			#except Exception, e:
			#	logger.error( unicode(e) )


############################################################
## Deploy script creation:

def create_deploy_script( extra_text, python_version = '' ):
	"""
	Creates a deploy script, which is like this script but with
	settings included

	This returns a string that (written to disk of course) can be used
	as a deploy script with your settings included. 
	"""
	filename = __file__
	if filename.endswith('.pyc'):
		filename = filename[:-1]
	f = open(filename, 'rb')
	content = f.read()
	f.close()
	py_exe = 'python%s' % python_version
	content = (('#!/usr/bin/env %s\n' % py_exe)
			   + '## WARNING: This file is generated\n'
			   + content)
	return content.replace('##EXT' 'END##', extra_text)

# -*- coding: utf-8 -*-
#
# djangoplicity-apptemplate
# Copyright (c) 2007-2011, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the European Southern Observatory nor the names 
#      of its contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE
#

"""
Script will be included into project bootstrap and deploy script and provides the settings 
and helper functions for both scripts.
"""

import sys
import os

PY_VERSION = "%s.%s" % ( sys.version_info[0], sys.version_info[1] )
VIRTUALENV_DIRNAME = 'virtualenv'

settings = {
	'vcs_base_dir' : 'projects',
	'vcs_projects' : [],
	'prompt' : None,
	'directories' : [
		'docs',		
		'docs_maintenance/',
		'projects',
		'virtualenv/apache',
		'virtualenv/etc',
		'logs',
		'tmp',
	],
	'symlinks' : [],
	'develop-symlinks' : [],
	'requirements' : [],
	'pre_install_tasks' : [],
	'post_install_tasks' : [],
	'finalize_tasks' : [],
	'requirements' :  [],
	'manage.py' : None,
}

			
# ==========================================
# Common tasks
# ==========================================
def task_vcs_install( base_dir, home_dir, bin_dir, options ):
	"""
	Install checked out VCS projects. Use the --develop option to install them as 
	editable.
	"""
	logger.notify("Installing VCS projects")
	
	vcs_base_dir = os.path.join( base_dir, _get_setting( 'vcs_base_dir', 'projects' ) )
	vcs_projects = _get_setting( 'vcs_projects', [] )

	for vcs_dirname, vcs_url in vcs_projects:
		try:
			vcs_dir = os.path.join( vcs_base_dir, vcs_dirname )
			if os.path.exists( os.path.join( vcs_dir, "setup.py" ) ):
				if options.develop:
					call_subprocess( [os.path.join( bin_dir, "pip" ), "install", "-E", home_dir, "-e", vcs_dir ] ) 
				else:
					call_subprocess( [os.path.join( bin_dir, "pip" ), "install", "-E", home_dir,  vcs_dir ] )
			else:
				logger.error( "Project located at %s has no setup.py file" % vcs_dir )
		except Exception, e:
			logger.error( unicode(e) )


def task_install_requirements( base_dir, home_dir, bin_dir ):
	"""
	Install all required Python modules 
	"""
	reqfiles = _get_setting('requirements')
	#repository = _get_setting('repository')
	if not reqfiles:
		logger.notify( "No requirements to install")
		return
	
	for reqdict in reqfiles:
		# Two supported formats: 
		# requirements = [{ 'file':'requirements.txt','repository':'http://...','options':['--no-index']},..]
		# or 
		# requirements = [requirements.txt',...]
		if issubclass( type(reqdict), dict ):
			reqfile = reqdict['file']
			repository = reqdict['repository'] if 'repository' in reqdict else None
			options = reqdict['options'] if 'options' in reqdict else None
		else:
			reqfile = reqdict
			repository = None
			options = None 
		
		reqfile = os.path.join( base_dir, reqdict['file'] )
		
		if not os.path.exists( reqfile ):
			logger.error("Requirements file %s does not exists" % reqfile )
			continue
		
		cmd = [os.path.join( bin_dir, "pip" ), "install"]
		if repository:
			logger.notify( "Using repository %s" % repository )
			cmd += ["--find-links", repository]
		if options:
			cmd += options
		cmd += ["-E", home_dir, "-r", reqfile] 
		
		logger.notify( "Installing packages defined in %s" % reqfile )
		try:
			call_subprocess( cmd )
		except Exception, e:
			logger.error( unicode(e) )


def task_run_manage(  base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, task=None ):
	"""
	Install checked out VCS projects. Use the --develop option to install them as 
	editable.
	"""
	if not task:
		logger.error("No task defined")
		return
	else:
		logger.notify("Running manage.py %s" % task)
	
	manage_py = _get_setting( 'manage.py', None )
	if not manage_py:
		logger.error("Setting 'manage.py' empty - please define path to manage.py.")
		
	manage_py_path = os.path.join( base_dir, manage_py )
	if os.path.exists( manage_py_path ):
		settings_module = _get_setting( 'settings_module', None )
		local_settings_module = options.local_settings
		
		if not settings_module:
			logger.error( "Settings 'settings_module' not defined" )
			return
		
		if not local_settings_module:
			local_settings_module = 'default_settings'
		
		try:
			os.environ['DJANGO_SETTINGS_MODULE'] = settings_module   
			os.environ['DJANGOPLICITY_SETTINGS'] = local_settings_module 
			call_subprocess( [ os.path.join( bin_dir, "python" ), manage_py_path, task ] ) 
		except Exception, e:
			logger.error( unicode(e) )
	else:
		logger.error( "Manage.py file %s does not exists" % manage_py_path )


def task_move(  base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, src=None, dst=None ):
	if not src or not dst:
		logger.errro("No source or destination defined")
		return
	
	src = os.path.join( base_dir, src )
	dst = os.path.join( base_dir, dst )
	logger.notify("Moving %s to %s" % (src,dst) )
	try:
		import shutil
		shutil.move( src, dst )
	except Exception, e:
		logger.error( unicode(e) )
	
	
def task_append( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, src=None, dst=None ):
	if not src or not dst:
		logger.errro("No source or destination defined")
		return
	
	src = os.path.join( base_dir, src )
	dst = os.path.join( base_dir, dst )
	logger.notify( "Appending %s to %s" % ( src, dst ) )
	try:
		f = open( src )
		append_text = f.read()
		f.close()
		
		f = open( dst, 'a' )
		f.write( append_text )
		f.close()
	except Exception, e:
		logger.error( unicode(e) )
# ==========================================
# Helper functions
# ==========================================
def _symlink( link_src, link_dest_path ):
	"""
	Create a symbolic link from source to destination
	"""
	link_dest_dir = os.path.dirname( link_dest_path )
	link_dest = os.path.basename( link_dest_path )
	
	if sys.platform == 'win32':
		logger.warn("Win32 platform detected - please create link yourself: %s to %s" % ( os.path.abspath( link_dest_path ), os.path.abspath( link_src ) ) )
		return
		
	if not os.path.lexists( link_dest_path ):
		logger.info( 'Creating symbolic link %s to %s.' % ( os.path.abspath( link_dest_path ), os.path.abspath( link_src ) ) )
		oldcwd = os.getcwd()
		os.chdir( link_dest_dir )
		# TODO: Extend to support win32
		os.symlink( link_src, link_dest )
		os.chdir(oldcwd)
	else:
		logger.warn( 'Symbolic link, %s, already exists ' % os.path.abspath( link_dest_path ) )
	
def _get_setting( attr, default=None ):
	"""
	Retrieve a settings value.
	"""
	if attr in settings:
		val = settings[attr]
		return default if val is None and default is not None else val
	else:
		return None

def _activate_virtualenv( bin_dir ):
	"""
	Activate the just installed virtual environment
	"""
	global logger
	if logger:
		logger.notify("Activating virtual environment")
	activate_this = os.path.join( bin_dir, "activate_this.py" )
	if os.path.exists( activate_this ):
		execfile( activate_this, dict( __file__ = activate_this ) )
	else:
		if logger:
			logger.error("Cannot activate virtual environment - bin/activate_this.py is missing.")
	

def run_script( script ):
	"""
	Return a function that will run the script. Script must be set as executable and should
	include the path from the base directory.
	"""
	def func( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options ):
		call_subprocess( [ os.path.join( base_dir, script ),  base_dir, home_dir, lib_dir, inc_dir, bin_dir ] )
	return func

def run_function( runfunc, **kwargs ):
	"""
	Return a function that will run the script. Script must be set as executable and should
	include the path from the base directory.
	"""
	def func( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options ):
		return runfunc( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, **kwargs )		
	return func
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
# Make sure the settings can be loaded in other modules
# 
if 'settings' not in globals():
	from djangoplicity.bootstrap.defaults import settings, PY_VERSION, run_function, task_move, task_append, task_run_manage
	 
	
#
# Requirements
#
requirements_repo = "http://www.djangoplicity.org/repository/packages/"
requirements_files = [{'file':'projects/spacetelescope.org/requirements.txt', 'repository':requirements_repo, 'options':['--no-index']}]

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
		run_function( task_move, src='tmp/conf/django.wsgi', dst='virtualenv/apache/' ),
		run_function( task_move, src='tmp/conf/httpd-djangoplicity.conf', dst='virtualenv/apache/'),
		run_function( task_append, src='tmp/conf/activate-djangoplicity.sh', dst='virtualenv/bin/activate'),
		run_function( task_append, src='tmp/conf/activate-djangoplicity.csh', dst='virtualenv/bin/activate.csh'), 
	]
}
settings.update( projects_settings )


if __name__ == '__main__':
	main()
