# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#


from djangoplicity.archives.feeds import DjangoplicityArchiveFeed
from models import *
from options import *

class AnnouncementFeed ( DjangoplicityArchiveFeed ):
	title = 'Hubble Announcements'
	link = '/announcements/'
	description = ''

	description_template = 'feeds/release_description.html'
	
	class Meta(DjangoplicityArchiveFeed.Meta):
		model = Announcement
		options = AnnouncementOptions
		latest_fieldname = Announcement.Archive.Meta.release_date_fieldname
		enclosure_resources = {	''   : 'resource_screen' }
		default_query = AnnouncementOptions.Queries.default
		category_query = None
		items_to_display = 10
		archive_query = "default"
		external_feed_url = "http://feeds.feedburner.com/hubble_announcements/"
			
		
	def item_enclosure_mime_type( self, item ):
		return 'image/jpeg'
	