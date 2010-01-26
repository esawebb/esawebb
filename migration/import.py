from django.conf import settings
from django.contrib.sites.models import Site
from djangoplicity.pages.models import Page, Section
from spacetelescope.migration import PageMigrationInitialization, PageMigration, SpacetelescopeDocument
	
conf = {
	'root' : '/Volumes/webdocs/spacetelescope/docs/',
	'default_site' : Site.objects.get(id=settings.SITE_ID),
	'default_section' : Section.objects.get_or_create( name='Default', append_title='spacetelescope.org', template='pages/page_onecolumn.html' )[0], 
}

migrations = [
	PageMigrationInitialization( conf ),
	PageMigration( conf, filename='images/index.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='projects/fits_liberator/news.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='jobs/index.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='pressroom/index.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='pressroom/mailinglist.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='pressroom/interview_possibilities.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='pressroom/video_formats.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='pressroom/image_formats.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='pressroom/presscoverage.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='copyright.html', docclass=SpacetelescopeDocument ),
	PageMigration( conf, filename='contact.html', docclass=SpacetelescopeDocument ),
]


if __name__ == "__main__":
	"""
	Run complete migration 
	"""
	state = {}
	for m in migrations:
		m.state = state
		m.migrate()
		state = m.state
		m.state = None