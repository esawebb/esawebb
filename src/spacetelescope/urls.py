# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from django.conf import settings
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from spacetelescope.admin import admin_site, adminlogs_site, adminshop_site


from djangoplicity.media.models import Image, Video, PictureOfTheWeek
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions
from django.views.generic.simple import redirect_to

from djangoplicity.releases.models import Release
from djangoplicity.releases.options import ReleaseOptions

from spacetelescope.archives.models import *
from spacetelescope.archives.options import *

from satchmo_store.urls import basepatterns

urlpatterns = []

urlpatterns += patterns( '',    

    # Djangoplicity Adminstration 
    ( r'^admin/cache/', include( 'djangoplicity.cache.urls', namespace="admincache_site", app_name="cache" ), { 'SSL': True } ),
    ( r'^admin/log/', include( 'djangoplicity.contrib.admin.log.urls', namespace="adminhistory_site", app_name="history" ), { 'SSL': True } ),
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ), { 'SSL': True } ),
    ( r'^admin/menus/', include( 'djangoplicity.menus.urls' ), { 'SSL' : True } ),
    ( r'^admin(.*)({{\s?MEDIA_URL\s?}})(?P<path>.*)', 'djangoplicity.views.adm_translate_static_media_path', { 'SSL' : True } ),
    ( r'^admin/shop/shop/order/(?P<order_id>[0-9]+)/csv/', 'djangoplicity.coposweb.views.order_csv_file', { 'SSL': True } ),
	( r'^admin/shop/', include(adminshop_site.urls), { 'SSL': True } ),
	( r'^admin/system/', include(adminlogs_site.urls), { 'SSL': True } ),
	( r'^admin/', include(admin_site.urls), { 'SSL': True } ),
	( r'^admin/import/', include('djangoplicity.archives.importer.urls'), { 'SSL': True } ),
	
	
    # Server alive check (used for load balancers - called every 5 secs )
    ( r'^alive-check.dat$', 'djangoplicity.views.alive_check', { 'SSLAllow' : True } ),
    ( r'^sitemap/', 'djangoplicity.menus.views.sitemap' ),

    # Media Archive
    ( r'^images/potw/', include('djangoplicity.media.urls_potw'), { 'model': PictureOfTheWeek, 'options': PictureOfTheWeekOptions } ),
	( r'^images/', include('djangoplicity.media.urls_images'), { 'model': Image, 'options': ImageOptions } ),
    #( r'^news/feed/(?P<url>.*)/?$', 'django.contrib.syndication.views.feed', { 'feed_dict': ReleaseOptions.get_feeds() } ),
    ( r'^news/', include('djangoplicity.releases.urls'), { 'model': Release, 'options': ReleaseOptions } ),
    ( r'^videos/uservideos/', include('spacetelescope.archives.urls.uservideos'), { 'model': UserVideo, 'options': UserVideoOptions } ),
    ( r'^videos/', include('djangoplicity.media.urls_videos'), { 'model': Video, 'options': VideoOptions } ),

	# Other archives
    ( r'^announcements/', include('spacetelescope.archives.urls.announcements'), { 'model': Announcement, 'options': AnnouncementOptions } ),
    ( r'^about/further_information/books/', include('spacetelescope.archives.urls.books'), { 'model': Book, 'options': BookOptions } ),
    ( r'^about/further_information/brochures/', include('spacetelescope.archives.urls.brochures'), { 'model': Brochure, 'options': BrochureOptions } ),
    ( r'^about/further_information/newsletters/', include('spacetelescope.archives.urls.newsletters'), { 'model': Newsletter, 'options': NewsletterOptions } ),
    ( r'^about/further_information/techdocs/', include('spacetelescope.archives.urls.techdocs'), { 'model': TechnicalDocument, 'options': TechnicalDocumentOptions } ),
	( r'^extras/calendars/', include('spacetelescope.archives.urls.calendars'), { 'model': Calendar, 'options': CalendarOptions } ),
	( r'^extras/art/', include('spacetelescope.archives.urls.art'), { 'model': OnlineArt, 'options': OnlineArtOptions } ),
	( r'^extras/artists/', include('spacetelescope.archives.urls.artists'), { 'model': OnlineArtAuthor, 'options': OnlineArtAuthorOptions } ),
    ( r'^extras/logos/', include('spacetelescope.archives.urls.logos'), { 'model': Logo, 'options': LogoOptions } ),
    ( r'^extras/conferenceposters/', include('spacetelescope.archives.urls.conference_posters'), { 'model': ConferencePoster, 'options': ConferencePosterOptions } ),
    ( r'^extras/exhibitions/', include('spacetelescope.archives.urls.exhibitions'), { 'model': Exhibition, 'options': ExhibitionOptions } ),
    ( r'^extras/stickers/', include('spacetelescope.archives.urls.stickers'), { 'model': Sticker, 'options': StickerOptions } ),
    ( r'^extras/postcards/', include('spacetelescope.archives.urls.postcards'), { 'model': PostCard, 'options': PostCardOptions } ),
    ( r'^extras/posters/', include('spacetelescope.archives.urls.posters'), { 'model': Poster, 'options': PosterOptions } ),
    ( r'^extras/merchandise/', include('spacetelescope.archives.urls.merchandise'), { 'model': Merchandise, 'options': MerchandiseOptions } ),
    ( r'^extras/dvds/', include('spacetelescope.archives.urls.cdroms'), { 'model': CDROM, 'options': CDROMOptions } ),
	( r'^extras/slideshows/', include('spacetelescope.archives.urls.slideshows'), { 'model': SlideShow, 'options': SlideShowOptions } ),
	#( r'^extras/printlayouts/', include('spacetelescope.archives.urls.printlayouts'), { 'model': Release, 'options': PrintLayoutOptions } ),
	( r'^extras/presentations/', include('spacetelescope.archives.urls.presentations'), { 'model': Presentation, 'options': PresentationOptions } ),
	( r'^kidsandteachers/education/', include('spacetelescope.archives.urls.education'), { 'model': EducationalMaterial, 'options': EducationalMaterialOptions } ),
	( r'^kidsandteachers/drawings/', include('spacetelescope.archives.urls.drawings'), { 'model': KidsDrawing, 'options': KidsDrawingOptions } ),
	( r'^press/kits/', include('spacetelescope.archives.urls.presskits'), { 'model': PressKit, 'options': PressKitOptions } ),
	
    ( r'^projects/fits_liberator/fitsimages/', include('spacetelescope.archives.urls.fitsimages'), { 'model': FITSImage, 'options': FITSImageOptions } ),
    
    ( r'^rss/feed.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'feed.xml' } ),
    ( r'^rss/vodcast.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'vodcast.xml' } ),
    ( r'^rss/vodcastfullhd.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'vodcastfullhd.xml' } ),
    ( r'^rss/vodcasthd.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'vodcasthd.xml' } ),
    

    # User authentication
    ( r'^login/$', 'djangoplicity.authtkt.views.login', { 'template_name': 'login.html', 'SSL' : True } ),
 	( r'^logout/$', 'djangoplicity.authtkt.views.logout', { 'template_name': 'logout.html', 'SSL' : True } ),
 	
 	# Main view
 	( r'^$', 'spacetelescope.views.main_page' ),
 )

urlpatterns += basepatterns + patterns('',
	# Satchmo Shop URLs
	(r'^shop/', include('satchmo_store.shop.urls')),
)

#handler404 = 'spacetelescope.views.page_not_found'


# Static files/media serving during development
if settings.SERVE_STATIC_MEDIA:
    urlpatterns += patterns( '',
        ( r'^' + settings.STATIC_MEDIA_PREFIX + r'/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True } ),
				)
