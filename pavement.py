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
import urllib
import shutil

import djangoplicity_paver.deploy
import djangoplicity_paver.svn

paver.setuputils.install_distutils_tasks()

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
							 '../projects/djangoplicity/apps/Jinja2-2.21.1.tar.gz',
							 '../projects/djangoplicity/apps/Pygments-1.2.2.tar.gz',
							 '../projects/djangoplicity/apps/Sphinx-0.6.4.tar.gz',
							 '../projects/djangoplicity/apps/MySQL-python-1.2.2-patched.tar.gz',
							 #'../projects/djangoplicity/apps/cmemcache-0.95-patched.tar.bz2',
							 '../projects/djangoplicity/apps/python-memcached-1.45.tar.gz',
                             '../projects/djangoplicity/apps/pycrypto-2.0.1.tar.gz',
							 '../projects/djangoplicity/apps/paramiko-1.7.4.tar.gz',
							 '../projects/djangoplicity/apps/fabric-0.9.0.tar.gz',
                             '../projects/djangoplicity/apps/BeautifulSoup.tar.gz',
                             #'../projects/djangoplicity/apps/threadpool-1.2.5.zip',
                             '../projects/djangoplicity/apps/Django-1.1.1.tar.gz',
                             #'../projects/djangoplicity/apps/Django-1.2-alpha-1.tar.gz',
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
                             '../projects/djangoplicity/apps/python-xmp-toolkit-1.0-rc1.tar.gz',
                             '../projects/djangoplicity/apps/python-avm-library-1.0a1.tar.gz',
                             
                             # Migration related packages.
                             '../projects/spacetelescope.org/apps/BareNecessities-0.2.4.tar.gz', 
                             '../projects/spacetelescope.org/apps/DreamweaverTemplate-0.1.1.tar.gz',
                             
                             ], # packages to install
        paver_command_line='', # command to run after installation
        unzip_setuptools = True,
    ),
      
    djangoplicity = Bunch(
        # Following two directories must exists.
        main_package = 'spacetelescope',
        virtualenv_dir = 'virtualenv',
        
        svn_projects_dir = 'projects',
        svn_projects = [ ('svn://svnsrv/p30/trunk/spacetelescope.org', 'spacetelescope.org'),
                         ('svn://svnsrv/p30/trunk/djangoplicity', 'djangoplicity' ),
                       ],
            
        rsync_dirs = [ ("projects/spacetelescope.org/static/","docs/static/" ),
					   ("projects/djangoplicity/static/","docs/static/djangoplicity/" ),
					   ("projects/spacetelescope.org/bin/","virtualenv/bin/"),
					 ],
        
        # Directories to create
        symlinks = [ ('../../virtualenv/lib/python2.5/site-packages/Django-1.1.1-py2.5.egg/django/contrib/admin/media', 'docs/static/', 'media' ), ],
		
        deploy_layout = [
                        'docs',
                        'docs/',
                        'docs/static/djangoplicity',
                        'docs/static/images/',
                        'docs/static/images/original',
						'docs/static/images/large',
						'docs/static/images/publicationtiff',
						'docs/static/images/publicationjpg',
						'docs/static/images/screen',
						'docs/static/images/wallpaper1',
						'docs/static/images/wallpaper2',
						'docs/static/images/wallpaper3',
						'docs/static/images/png',
						'docs/static/images/eps',
						'docs/static/images/illustrator',
						'docs/static/images/illustrator_text',
						'docs/static/images/news',
						'docs/static/images/newsmini',
						'docs/static/images/hofthumbs',
						'docs/static/images/medium',
						'docs/static/images/mini',
						'docs/static/images/wallpaperthumbs',
						'docs/static/images/thumbs',
						'docs/static/images/zoomable',
						'docs/static/images/frontpagethumbs',
						'docs/static/images/potw',
						'docs/static/videos/',
						'docs/static/videos/newsfeature',
						'docs/static/videos/thumb',
						'docs/static/videos/newsmini',
						'docs/static/videos/frontpagethumb',
						'docs/static/videos/newsfeature',
						'docs/static/videos/videoframe',
						'docs/static/videos/mini',
						'docs/static/videos/script',
						'docs/static/videos/small_flash',
						'docs/static/videos/small_qt',
						'docs/static/videos/medium_podcast',
						'docs/static/videos/medium_mpeg1',
						'docs/static/videos/medium_flash',
						'docs/static/videos/large_qt',
						'docs/static/videos/broadcast_sd',
						'docs/static/videos/broadcast_sd_old',
						'docs/static/videos/hd_and_apple',
						'docs/static/videos/hd_broadcast_720p25',
						'docs/static/videos/hd_broadcast_720p50',
						'docs/static/videos/hd_1080p25_screen',
						'docs/static/videos/hd_1080p25_broadcast',
						'docs/static/videos/dome_master',
						'docs/static/releases/',
						'docs/static/releases/doc',
						'docs/static/releases/text',
						'docs/static/releases/pdf',
						'docs/static/releases/sciencepapers',
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