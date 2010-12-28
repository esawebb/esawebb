# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from paver.easy import *
from paver.setuputils import *
import paver.doctools
import paver.virtual
import setuptools
import paver.svn
import os
import sys
import urllib
import shutil

import djangoplicity_paver.deploy
import djangoplicity_paver.svn

paver.setuputils.install_distutils_tasks()

PY_VERSION = "%s.%s" % (sys.version_info[0],sys.version_info[1])

# Ensure we can use the file as standalone.
try:
	srcpackages = setuptools.find_packages('src')
except OSError:
	srcpackages = []

#
# Paver Options
#    
options(
    setup = Bunch(
        name = 'spacetelescope',
        version = djangoplicity_paver.svn.get_svn_revision(),
        description = 'spacetelescope.org website',
        author = 'European Southern Observatory',
        author_email = 'lnielsen@eso.org',

        zip_safe = False,
        
        packages = srcpackages,
        package_dir = { '': 'src' },
        include_package_data = True,        
        install_requires = [],
    ),
    
    sphinx = Bunch(
        docroot = 'docs',
        builddir = 'build',
        sourcedir = '',
    ),  
    
    virtualenv = Bunch(
        script_name = 'setup_virtualenv.py',
        
        # Paths relative to virtualenv dir
        packages_to_install=['../projects/djangoplicity/apps/Paver-1.0.1.tar.gz',
							 '../projects/djangoplicity/apps/virtualenv-1.4.4.tar.gz',
							 '../projects/djangoplicity/apps/docutils-0.6.tar.gz',
							 '../projects/djangoplicity/apps/Jinja2-2.5.tar.gz',
							 '../projects/djangoplicity/apps/Pygments-1.2.2.tar.gz',
							 '../projects/djangoplicity/apps/Sphinx-0.6.4.tar.gz',
							 '../projects/djangoplicity/apps/MySQL-python-1.2.2-patched.tar.gz',
							 #'../projects/djangoplicity/apps/cmemcache-0.95-patched.tar.bz2',
							 '../projects/djangoplicity/apps/python-memcached-1.45.tar.gz',
                             '../projects/djangoplicity/apps/pycrypto-2.1.0.tar.gz',
							 '../projects/djangoplicity/apps/paramiko-1.7.4.tar.gz',
							 '../projects/djangoplicity/apps/Fabric-0.9.1.tar.gz',
                             '../projects/djangoplicity/apps/BeautifulSoup.tar.gz',
                             #'../projects/djangoplicity/apps/threadpool-1.2.5.zip',
                             '../projects/djangoplicity/apps/Django-1.2.4.tar.gz',
                             '../projects/djangoplicity/apps/django-extensions-0.4.1.tar.gz',
                             '../projects/djangoplicity/apps/django-confutils-1.0-dev.tar.gz',
                             #'../projects/djangoplicity/apps/django-batchadmin-0.1.tar.gz',
                             '../projects/djangoplicity/apps/django-mptt-0.3_pre.tar.gz',
                             '../projects/djangoplicity/apps/djangodblog-1.0.tar.gz',
                             '../projects/djangoplicity/apps/django-debug-toolbar-0.8.1.zip',
                             '../projects/djangoplicity/apps/django-assets-0.2.zip',
                             '../projects/djangoplicity/apps/django-sslmiddleware-dev.tar.gz',
                             #'../projects/djangoplicity/apps/django-spambayes-0.1.tar.gz',
                             '../projects/djangoplicity/apps/recaptcha-client-1.0.3.tar.gz',
                             '../projects/djangoplicity/apps/cssutils-0.9.6b2.tar.gz',
                             '../projects/djangoplicity/apps/amqplib-0.6.1.tar.gz',
                             '../projects/djangoplicity/apps/anyjson-0.2.1.tar.gz',
                             '../projects/djangoplicity/apps/lockfile-0.8.tar.gz',
                             '../projects/djangoplicity/apps/multiprocessing-2.6.1.1.tar.gz',
                             '../projects/djangoplicity/apps/django-unittest-depth-0.6.tar.gz',
                             '../projects/djangoplicity/apps/python-daemon-1.5.1.tar.gz',
                             '../projects/djangoplicity/apps/carrot-0.6.0.tar.gz',
                             '../projects/djangoplicity/apps/celery-0.8.0-patched.tar.gz',
                             '../projects/djangoplicity/apps/python-dateutil-1.5.tar.gz',
                             '../projects/djangoplicity/apps/python-xmp-toolkit-1.0-rc2.tar.gz',
                             '../projects/djangoplicity/apps/python-avm-library-1.0b1.tar.gz',
                             '../projects/djangoplicity/apps/django-rosetta-0.5.5.tar.gz',
                                                          
                             # Migration related packages.
                             '../projects/spacetelescope.org/apps/BareNecessities-0.2.4.tar.gz', 
                             '../projects/spacetelescope.org/apps/DreamweaverTemplate-0.1.1.tar.gz',
                             
							 # Satchmo packages
							 '../projects/djangoplicity/apps/trml2pdf-1.2.tar.gz',
							 '../projects/djangoplicity/apps/setuptools_hg-0.2.tar.gz',
							 '../projects/djangoplicity/apps/sorl-thumbnail-3.2.5.tar.gz',
							 '../projects/djangoplicity/apps/PyYAML-3.09.zip',
							 '../projects/djangoplicity/apps/django-livesettings-1.4-3.tar.gz',
							 '../projects/djangoplicity/apps/django-registration-0.7.tar.gz',
							 '../projects/djangoplicity/apps/django-signals-ahoy-0.1-1.tar.gz',
							 '../projects/djangoplicity/apps/django-caching-app-plugins-0.1.1.tar.gz',
							 '../projects/djangoplicity/apps/django-keyedcache-1.4-2.tar.gz',
							 '../projects/djangoplicity/apps/django_threaded_multihost-1.3_2-py2.5.egg',
							 '../projects/djangoplicity/apps/reportlab-2.4.tar.gz',
							 '../projects/djangoplicity/apps/satchmo-v0.9.1.zip',
							 '../projects/djangoplicity/apps/ssl-1.15-patched.tar.gz',
                             
                             ], # packages to install
        paver_command_line='', # command to run after installation
        unzip_setuptools = True,
    ),
      
    djangoplicity = Bunch(
        # Following two directories must exists.
        main_package = 'spacetelescope',
        virtualenv_dir = 'virtualenv',
        
        svn_projects_dir = 'projects',
        svn_projects = [ ('http://svnhq30.hq.eso.org/p30/trunk/spacetelescope.org', 'spacetelescope.org'),
                         ('http://svnhq30.hq.eso.org/p30/trunk/djangoplicity', 'djangoplicity' ),
                       ],
            
        rsync_dirs = [ ("projects/spacetelescope.org/static/","docs/static/" ),
					   ("projects/djangoplicity/static/","docs/static/djangoplicity/" ),
					   ("projects/spacetelescope.org/bin/","virtualenv/bin/"),
					 ],
        
        # Directories to create
        symlinks = [ ('../../virtualenv/lib/python%(version)s/site-packages/Django-1.2.4-py%(version)s.egg/django/contrib/admin/media' % { 'version' : PY_VERSION }, 'docs/static/', 'media' ),],
        deploy_layout = [
                        'docs',
                        'docs/static',
                        'docs/static/djangoplicity',
                        'docs/static/archives',
                        'docs/static/archives/images/',
                        'docs/static/archives/images/original',
						'docs/static/archives/images/large',
						'docs/static/archives/images/publicationtiff',
						'docs/static/archives/images/publicationjpg',
						'docs/static/archives/images/screen',
						'docs/static/archives/images/wallpaper1',
						'docs/static/archives/images/wallpaper2',
						'docs/static/archives/images/wallpaper3',
						'docs/static/archives/images/png',
						'docs/static/archives/images/eps',
						'docs/static/archives/images/illustrator',
						'docs/static/archives/images/illustrator_text',
						'docs/static/archives/images/news',
						'docs/static/archives/images/newsmini',
						'docs/static/archives/images/hofthumbs',
						'docs/static/archives/images/medium',
						'docs/static/archives/images/mini',
						'docs/static/archives/images/wallpaperthumbs',
						'docs/static/archives/images/thumbs',
						'docs/static/archives/images/zoomable',
						'docs/static/archives/images/frontpagethumbs',
						'docs/static/archives/images/potw',
						'docs/static/archives/videos/',
						'docs/static/archives/videos/newsfeature',
						'docs/static/archives/videos/thumb',
						'docs/static/archives/videos/newsmini',
						'docs/static/archives/videos/frontpagethumb',
						'docs/static/archives/videos/newsfeature',
						'docs/static/archives/videos/videoframe',
						'docs/static/archives/videos/mini',
						'docs/static/archives/videos/script',
						'docs/static/archives/videos/small_flash',
						'docs/static/archives/videos/small_qt',
						'docs/static/archives/videos/medium_podcast',
						'docs/static/archives/videos/medium_mpeg1',
						'docs/static/archives/videos/medium_flash',
						'docs/static/archives/videos/large_qt',
						'docs/static/archives/videos/broadcast_sd',
						'docs/static/archives/videos/broadcast_sd_old',
						'docs/static/archives/videos/hd_and_apple',
						'docs/static/archives/videos/hd_broadcast_720p25',
						'docs/static/archives/videos/hd_broadcast_720p50',
						'docs/static/archives/videos/hd_1080p25_screen',
						'docs/static/archives/videos/hd_1080p25_broadcast',
						'docs/static/archives/videos/dome_master',
						'docs/static/archives/releases/',
						'docs/static/archives/releases/doc',
						'docs/static/archives/releases/text',
						'docs/static/archives/releases/pdf',
						'docs/static/archives/releases/sciencepapers',
						'docs_maintenance/',
                        'projects',
                        'virtualenv',
                        'virtualenv/apache',
                        'logs',
                        'tmp',
                        ],
		
        pre_install_scripts = [ 'projects/djangoplicity/apps/install_pil.sh',
					  	        'projects/djangoplicity/apps/install_geoip.sh',
                                #'projects/djangoplicity/apps/install_exempi.sh',
                              ],
		
		post_install_scripts = ['projects/spacetelescope.org/scripts/fixperms.sh',
							  ],
                           
        env_vars = [ 'PATH="%s/bin:$PATH"',
				     'LDFLAGS="-L%s/lib -L/home/web/lib -L/home/web/lib/mysql"',
					 'CPPFLAGS="-I%s/include -I/home/web/include"',
					 'CFLAGS="-I%s/include -I/home/web/include"',
					 'LD_LIBRARY_PATH="%s/lib:/home/web/lib:/home/web/lib/mysql:$LD_LIBRARY_PATH"',
				],
                
        # Alternate values used for "paver deploy_develop"           
        _develop = Bunch(
                            deploy_layout = [
                             'docs',
                             'projects',
                             'virtualenv',
                             'virtualenv/apache',
                             'logs',
                             'tmp',
                            ],
                            
                            symlinks = [('../../../pttu/spacetelescope.org', 'projects/', 'spacetelescope.org' ),
                                        ('../../../pttu/djangoplicity', 'projects/', 'djangoplicity' ),
                                        ('../../../pttu/spacetelescope.org/static', 'docs', 'static' ),
                                        ('../../../pttu/djangoplicity/static', 'docs/static', 'djangoplicity' ),
                                        ],
                                        
                            rsync = [],
                            
                            post_install_scripts = [],
                            
                            env_vars = [ 'PATH="%s/bin:$PATH"',
									     'LDFLAGS="-L%s/lib"',
										 'CPPFLAGS="-I%s/include"',
										 'CFLAGS="-I%s/include"',
										 'LD_LIBRARY_PATH="%s/lib:$LD_LIBRARY_PATH"',
										 'DYLD_LIBRARY_PATH="%s/lib:$DYLD_LIBRARY_PATH"',
									],
                        )
    )
)