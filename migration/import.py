from django.conf import settings
from django.contrib.sites.models import Site
from djangoplicity.logger import define_logger
from djangoplicity.migration import run_migration
from djangoplicity.migration.apps.pages import PageInitializationTask, \
	PageMigrationTask
from djangoplicity.pages.models import Section
from spacetelescope.migration.pages import SpacetelescopePageDocument
import logging

#
# Define logger to use
#
logger = define_logger( "migration_logger", level=logging.DEBUG, file_logging=False )
	
#
# Define configuration options
#
conf = {
	'pages' : {
				'root' : '/Volumes/webdocs/spacetelescope/docs/', 
				'site' : Site.objects.get(id=settings.SITE_ID), 
				'section' : Section.objects.get_or_create( name='Default', append_title='spacetelescope.org', template='pages/page_onecolumn.html' )[0] 
			  },
	'logger' : 'migration_logger', 
}

#
# Define migration tasks
#
tasks = [
	PageInitializationTask(),
	PageMigrationTask( SpacetelescopePageDocument( 'images/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/news.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'jobs/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/mailinglist.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/interview_possibilities.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/video_formats.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/image_formats.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/presscoverage.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'copyright.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'contact.html' ) ), 
]

if __name__ == "__main__":
	"""
	Run complete migration 
	"""
	run_migration( conf, tasks )