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
import virtualenv
from virtualenv import Logger, make_environment_relocatable, path_locations, mkdir
from pip import call_subprocess

logger = Logger([(Logger.LEVELS[-1], sys.stdout)])

def main():
	parser = optparse.OptionParser( usage="%prog [OPTIONS] DEST_DIR" )

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
		help = 'Decrease verbosity'
	)
	
	EXCLUDE = []

	if 'extend_parser' in globals():
		extend_parser( parser, exclude=EXCLUDE )

	options, args = parser.parse_args()
	
	global logger

	if 'adjust_options' in globals():
		adjust_options( options, args, exclude=EXCLUDE )
		
	verbosity = options.verbose - options.quiet
	logger = Logger( [( Logger.level_for_integer( 2 - verbosity ), sys.stdout )] )
	
	# Ensure virtualenv will not complain about missing defined logger.
	virtualenv.logger = logger
	
	if not args:
		print 'You must provide a DEST_DIR'
		parser.print_help()
		sys.exit(2)
	if len(args) > 1:
		print 'There must be only one argument: DEST_DIR (you gave %s)' % (
			' '.join(args))
		parser.print_help()
		sys.exit(2)
	
	home_dir = args[0]
	
	if 'settings' not in globals() or 'VIRTUALENV_DIRNAME' not in globals():
		print 'Invalid script - no settings included in script.'
		sys.exit(3)
	
	if 'after_install' in globals():
		after_install( options, home_dir, title="Deployment tasks", activate=True )

# =======================================================
# Deploy script creation:
# =======================================================
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
import time

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


# =======================================================
# Hooks for virtualenv bootstrap script and deploy script
# =======================================================
start_time = None

def extend_parser( parser, exclude=[] ):
	"""
	Add extra options to the parser
	"""
	global start_time
	start_time = time.time()
	
	if 'tag' not in exclude:
		parser.add_option( '-t', '--tag', action = 'store', dest = 'tag', default = None, help = "Deploy specific tag existing on all VCS projects" )
	if 'existing-checkout' not in exclude:
		parser.add_option( "--existing-checkout", dest='existing_checkout_dir', metavar="DIR", action='store', default=None, help='Path to already existing checkout of VCS projects. This is mostly used together with the --develop option.' )
	if 'develop' not in exclude:
		parser.add_option( "--develop", dest='develop', action='store_true', default=False, help='Install VCS projects in editable mode and create develop only symbolic links.' )
	if 'delete' not in exclude:
		parser.add_option( "--delete", dest='delete', action='store_true', default=False, help='Delete this script after bootstrapping.' )
	if 'local-settings' not in exclude:
		parser.add_option( "--local-settings", dest='local_settings', metavar="MODULE", action='store', default=None, help='Local settings module to use - e.g production_settings.' )
	if 'relocate-to' not in exclude:
		parser.add_option( "--relocate-to", dest='relocate_to', metavar="DIR", action='store', default=None, help='Path to relocate virtualenv to.' )


def adjust_options( options, args, exclude=[] ):
	"""
	Adjust options and args of bootstrap script to ensure it can be called without arguments
	"""
	if not args:
		# If no args are giving then run bootstrap in current directory.
		args.append( os.path.dirname( os.path.abspath( __file__ ) ) )
	
	# Build virtualenv in a subdirectory.
	base_dir = args[0]
	args[0] = os.path.join( base_dir, VIRTUALENV_DIRNAME )
	
	# Set default options and remove possibility to set them
	try:
		options.no_site_packages = True
		options.clear = True
		options.use_distribute = True
		options.unzip_setuptools = True
		options.prompt = "(%s) " % _get_setting( 'prompt', VIRTUALENV_DIRNAME )
	except AttributeError:
		pass
	
	if 'existing-checkout' not in exclude and options.existing_checkout_dir:
		tmppath = os.path.abspath( os.path.expandvars( os.path.expanduser( options.existing_checkout_dir ) ) )
		options.existing_checkout_dir = tmppath if os.path.exists( tmppath ) else None
	if 'relocate-to' not in exclude and options.relocate_to:
		options.relocate_to = options.relocate_to if os.path.exists( options.relocate_to ) else None
		
	# Modify project settings if specific tag has been specified
	if 'tag' not in exclude and options.tag:
		if 'vcs_projects' in settings:
			tmp = [] 
			for prj,url in settings['vcs_projects']:
				tmp.append( (prj, "%s@%s" % (url, options.tag) ) )
			settings['vcs_projects'] = tmp
		

def after_install( options, home_dir, title = "Post install tasks", activate=True ):
	"""
	Entry point for post-install actions after virtualenv have been setup. 
	"""
	logger.notify("")
	logger.notify( title )
	logger.notify( "="*len( title ) )

	# Setup bin dir
	home_dir, lib_dir, inc_dir, bin_dir = path_locations( home_dir ) # path_locations defined in virtualenv
	base_dir = os.path.dirname( home_dir )
	
	# Activate the virutal environment
	if activate:
		_activate_virtualenv( bin_dir )
	
	# Run tasks
	task_create_directories( base_dir )
	task_create_symlinks( base_dir )
	task_vcs_checkout_update( base_dir, options )
	if options.develop:
		task_create_symlinks( base_dir, setting='develop-symlinks' )
	task_hooks( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, setting_name='pre_install_tasks' ) 
	task_install_requirements( base_dir, home_dir, bin_dir )
	task_hooks( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, setting_name='post_install_tasks' )
	task_vcs_install( base_dir, home_dir, bin_dir, options )
	make_environment_relocatable( home_dir )
	# Activate the virutal environment (needed to make all installed packages available for hooks).
	if activate:
		_activate_virtualenv( bin_dir )
	task_hooks( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, setting_name='finalize_tasks' )
	fixup_activate_scripts( home_dir, bin_dir, options ) # Fix up last, otherwise tasks depending on activate scripts will not run
	if options.delete:
		logger.notify( "Removing bootstrap/deploy script" )
		os.remove( __file__ )
	
	if start_time:
		delta = time.time() - start_time
		logger.notify("Bootstrap/deploy took %0.0f s" % delta )


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
					call_subprocess( [os.path.join( bin_dir, "pip" ), "install", "-I", "-U", "-E", home_dir, "-e", vcs_dir ] ) 
				else:
					call_subprocess( [os.path.join( bin_dir, "pip" ), "install", "-I", "-U", "-E", home_dir,  vcs_dir ] )
			else:
				logger.error( "Project located at %s has no setup.py file" % vcs_dir )
		except Exception, e:
			logger.error( unicode(e) )


def task_vcs_checkout_update( base_dir, options ):
	"""
	Retrieve projects from version control system (using pip for checkout)
	"""
	logger.notify("Running version controls checkout/updates")
	
	vcs_base_dir = os.path.join( base_dir, _get_setting( 'vcs_base_dir', 'projects' ) )
	vcs_projects = _get_setting( 'vcs_projects', [] )
	
	if not os.path.exists( vcs_base_dir ):
		logger.warn("VCS base directory %s doesn't exists, so it will be created")
		try:
			os.makedirs( vcs_base_dir )
		except Exception, e:
			logger.error( unicode(e) )
	
	if vcs_projects:
		# Register all version control modules
		try:
			from pip import version_control
			version_control()
		except ImportError:
			from pip import import_vcs_support
			import_vcs_support()
		
		from pip.vcs import vcs
		
		# Loop over projects
		for vcs_dirname, vcs_url in vcs_projects:
			vcs_dir = os.path.join( vcs_base_dir, vcs_dirname )
			
			# Check out or use already existing checkouts?
			if options.existing_checkout_dir:
				# Link to existing project
				existing_vcs_dir = os.path.join( options.existing_checkout_dir, vcs_dirname )
				
				try:
					_symlink( existing_vcs_dir, vcs_dir )
				except Exception, e:
					logger.error( unicode(e) )
					
				if not os.path.exists( existing_vcs_dir ):
					logger.info( "Existing VCS project doesn't exists at %s" % existing_vcs_dir )
					vcs_dir = existing_vcs_dir
				else:
					vcs_dir = None

			if vcs_dir:
				print vcs_dir
				# Checkout/update project
				try:
					vc_type, url = vcs_url.split( '+', 1 )
					backend = vcs.get_backend( vc_type )
					if backend:
						logger.info( "Retrieving VCS project from URL %s " % vcs_url )
						vcs_backend = backend( vcs_url )
						if os.path.exists( vcs_dir ):
							url, rev = vcs_backend.get_url_rev()
							rev_options = [rev] if rev else []
							vcs_backend.update( vcs_dir, rev_options )
						else: 
							vcs_backend.obtain( vcs_dir )
					else:
						logger.error( "Unexpected version control type (in %s): %s" % ( url, vc_type ) )
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


def task_move(  base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, src=None, dst=None, remove_dst=True ):
	if not src or not dst:
		logger.errro("No source or destination defined")
		return
	
	src = os.path.join( base_dir, src )
	dst = os.path.join( base_dir, dst )
	
	# Normalize dst
	logger.notify("Moving %s to %s" % (src,dst) )
	
	try:
		import shutil
		dstpath = os.path.join( dst, os.path.basename( src ) )
		if os.path.exists( dstpath ):
			if remove_dst:
				logger.notify( "Destination %s already exists - removing. " % ( dstpath ) )
				if os.path.isdir( dstpath ):
					shutil.rmtree( dstpath )
				else:
					os.remove( dstpath )
			else:
				logger.error( "Destination % already exists." % ( dstpath ) )
				return

		shutil.move( src, dst )
	except Exception, e:
		logger.error( unicode(e) )
	
	



def task_append( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, src=None, dst=None, marker=None, settings_module=None ):
	if not src or not dst:
		logger.error("No source or destination defined")
		return
	
	src = os.path.join( base_dir, src )
	dst = os.path.join( base_dir, dst )
	logger.notify( "Appending %s to %s" % ( src, dst ) )
	try:
		f = open( src )
		append_text = f.read()
		f.close()
		
		# If settings_module is provided (e.g "photoshop-celeryworker" or "spacetelescope", i.e a moduel with a conf
		# package that can be loaded by djangoplicity-settings), then the local settings module specified on 
		# the command-line will be used to substitute template variables in the src file, before being appended
		# to the destination file.
		if settings_module:
			try:
				from djangoplicity.settings import import_settings
				settings_mod = import_settings( settings_module, local_settings_module=options.local_settings )
				settings_ctx = dict( filter( lambda x: not x[0].startswith( "_" ), settings_mod.__dict__.items() ) )
				append_text = append_text % settings_ctx
			except ImportError, e:
				logger.error( "task_append: settings_module can only be used if djangoplicity.settings is installed." )
				
		if marker is None:
			marker = src
		text = _insert_section( dst, append_text, marker )
		
		f = open( dst, 'w+' )
		f.write( text )
		f.close()
	except Exception, e:
		logger.error( unicode(e) )
		

def task_create_directories( base_dir ):
	"""
	Task for creating directories.
	"""
	logger.notify("Creating directories in deployment root")
	directories = _get_setting( 'directories', [] )
	
	for p in directories:
		try:
			mkdir( os.path.join( base_dir, p ) )
		except Exception, e:
			logger.error( unicode(e) )
		

def task_create_symlinks( base_dir, setting='symlinks' ):
	"""
	Task for creating symlinks
	"""
	if sys.platform == 'win32':
		logger.warn("Windows doesn't support os.symlink so please make the following link yourself:")
	else:
		logger.notify("Creating symlinks in deployment root")
	symlinks = _get_setting( setting, [] )
	
	for link_src, link_dest in symlinks:
		link_dest = os.path.join( base_dir, link_dest )
		try:
			_symlink( link_src, link_dest )
		except Exception, e:
			logger.error( unicode(e) )
	os.chdir( base_dir )

	
def task_hooks( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options, setting_name=None ):
	"""
	Execute a number of callables that may be user-defined. 
	"""
	hooks = _get_setting( setting_name, [] )
	if hooks:
		logger.notify("Running %s hooks" % setting_name )
	
	for func in hooks:
		if callable( func ):
			try:
				func( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options )
			except Exception, e:
				logger.error( unicode(e) )	

def fixup_activate_scripts( home_dir, bin_dir, options ):
	if not options.relocate_to:
		return
	
	scripts_fixup = ( "activate", "activate.fish", "activate.csh" )

	for filename in os.listdir( bin_dir ):
		if filename not in scripts_fixup:
			continue #ignoring all scripts known not to need fixup.
		filename = os.path.join( bin_dir, filename )
		f = open( filename, 'rb' )
		lines = f.readlines()
		f.close()
		if not lines:
			logger.warn( 'Script %s is an empty file' % filename )
			continue
		
		import re
		replacement = False		
		newlines = []
		p = re.compile( home_dir )
		for l in lines:
			m = p.search( l )
			if m:
				l = p.sub( os.path.join( options.relocate_to, VIRTUALENV_DIRNAME ), l )
				replacement = True				
			newlines.append( l )
		
		if replacement:
			logger.notify( 'Making script %s relative' % filename )
			f = open( filename, 'wb' )
			f.writelines( newlines )
			f.close()

# ==========================================
# Helper functions
# ==========================================
def _insert_section( src, text, marker, start_comment="#", end_comment="" ):
	f = open( src )
	content = f.readlines()
	f.close()
	
	final_content = ""
	include = True
	touched = False
	
	start_mark = "%s## BEGIN: %s ###%s\n" % ( start_comment, marker, end_comment )
	end_mark = "%s## END: %s ###%s\n" % ( start_comment, marker, end_comment )
	
	for l in content:
		if include:
			final_content += l
			
		if l == start_mark:
			final_content += text
			touched = True
			include = False
			
		if l == end_mark:
			final_content += end_mark
			include = True
		
	if not touched:	
		final_content += "\n%s" % start_mark
		final_content += text
		final_content += "\n%s" % end_mark
	
	return final_content
		

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
	

def run_script( script, args=[] ):
	"""
	Return a function that will run the script. Script must be set as executable and should
	include the path from the base directory.
	"""
	def func( base_dir, home_dir, lib_dir, inc_dir, bin_dir, options ):
		ctx = { "base_dir" : base_dir, "home_dir" : home_dir, "lib_dir" : lib_dir, "inc_dir" : inc_dir, "bin_dir" : bin_dir }
		cmd = [ script % ctx ]
		for a in args:
			cmd.append(a % ctx)
		call_subprocess( cmd )
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
# Make sure the settings can be loaded in other modules (currently fabfile.py, deploy.py and bootstrap.py)
# 
if 'settings' not in globals():
	from djangoplicity.bootstrap.defaults import settings, PY_VERSION, run_function, task_move, task_append, task_run_manage, run_script
	 
	
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
			( 'djangoplicity-admincomments', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-admincomments' ),
			( 'djangoplicity-fabric', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-fabric',),
			( 'djangoplicity-social', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-social',),
			( 'djangoplicity-newsletters', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-newsletters',),
			( 'djangoplicity-actions', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-actions',),
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
			'import',
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
		run_script( "%(bin_dir)s/python", args=[ "%(base_dir)s/projects/djangoplicity/scripts/archive.create.dirs.py" ] ),
	]
}
settings.update( projects_settings )


if __name__ == '__main__':
	main()
