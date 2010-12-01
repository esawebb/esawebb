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

from djangoplicity.announcements.models import Announcement
from djangoplicity.announcements.options import AnnouncementOptions
from djangoplicity.media.models import Image, Video, PictureOfTheWeek
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions
from django.views.generic.simple import redirect_to

from djangoplicity.products.models import *
from djangoplicity.products.options import *

from djangoplicity.releases.models import Release
from djangoplicity.releases.options import ReleaseOptions

from djangoplicity.products.models import *
from djangoplicity.products.options import *

urlpatterns = []

urlpatterns += patterns( '',    

    # Djangoplicity Adminstration 
    ( r'^admin/cache/', include( 'djangoplicity.cache.urls', namespace="admincache_site", app_name="cache" ), { 'SSL': True } ),
    ( r'^admin/log/', include( 'djangoplicity.contrib.admin.log.urls', namespace="adminhistory_site", app_name="history" ), { 'SSL': True } ),
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ), { 'SSL': True } ),
    ( r'^admin/menus/', include( 'djangoplicity.menus.urls' ), { 'SSL' : True } ),
    ( r'^admin(.*)({{\s?MEDIA_URL\s?}})(?P<path>.*)', 'djangoplicity.views.adm_translate_static_media_path', { 'SSL' : True } ),
    ( r'^admin/shop/shop/order/(?P<order_id>[0-9]+)/csv/', 'djangoplicity.coposweb.views.order_csv_file', { 'SSL': True } ),
	( r'^admin/shop/', include( 'djangoplicity.archives.contrib.satchmo.urls_admin' ), { 'SSL': True } ), 
	( r'^admin/shop/', include(adminshop_site.urls), { 'SSL': True, 'extra_context' : { 'ADMINSHOP_SITE' : True } } ),
	( r'^admin/system/', include(adminlogs_site.urls), { 'SSL': True, 'extra_context' : { 'ADMINLOGS_SITE' : True }  } ),
	( r'^admin/', include(admin_site.urls), { 'SSL': True, 'extra_context' : { 'ADMIN_SITE' : True }  } ),
	( r'^admin/import/', include('djangoplicity.archives.importer.urls'), { 'SSL': True } ),
	
    # Server alive check (used for load balancers - called every 5 secs )
    ( r'^alive-check.dat$', 'djangoplicity.views.alive_check', { 'SSLAllow' : True } ),
    ( r'^sitemap/', 'djangoplicity.menus.views.sitemap' ),

    # Media Archive
    ( r'^images/potw/', include('djangoplicity.media.urls_potw'), { 'model': PictureOfTheWeek, 'options': PictureOfTheWeekOptions } ),
	( r'^images/', include('djangoplicity.media.urls_images'), { 'model': Image, 'options': ImageOptions } ),
    #( r'^news/feed/(?P<url>.*)/?$', 'django.contrib.syndication.views.feed', { 'feed_dict': ReleaseOptions.get_feeds() } ),
    ( r'^news/', include('djangoplicity.releases.urls'), { 'model': Release, 'options': ReleaseOptions } ),
    ( r'^videos/uservideos/', include('djangoplicity.products.urls.uservideos'), { 'model': UserVideo, 'options': UserVideoOptions } ),
    ( r'^videos/', include('djangoplicity.media.urls_videos'), { 'model': Video, 'options': VideoOptions } ),

	# Other archives
    ( r'^announcements/', include('djangoplicity.announcements.urls'), { 'model': Announcement, 'options': AnnouncementOptions } ),
    ( r'^about/further_information/books/', include('djangoplicity.products.urls.books'), { 'model': Book, 'options': BookOptions } ),
    ( r'^about/further_information/brochures/', include('djangoplicity.products.urls.brochures'), { 'model': Brochure, 'options': BrochureOptions } ),
    ( r'^about/further_information/newsletters/', include('djangoplicity.products.urls.newsletters'), { 'model': Newsletter, 'options': NewsletterOptions } ),
    ( r'^about/further_information/techdocs/', include('djangoplicity.products.urls.techdocs'), { 'model': TechnicalDocument, 'options': TechnicalDocumentOptions } ),
	( r'^extras/calendars/', include('djangoplicity.products.urls.calendars'), { 'model': Calendar, 'options': CalendarOptions } ),
	( r'^extras/art/', include('djangoplicity.products.urls.art'), { 'model': OnlineArt, 'options': OnlineArtOptions } ),
	( r'^extras/artists/', include('djangoplicity.products.urls.artists'), { 'model': OnlineArtAuthor, 'options': OnlineArtAuthorOptions } ),
    ( r'^extras/logos/', include('djangoplicity.products.urls.logos'), { 'model': Logo, 'options': LogoOptions } ),
    #( r'^extras/conferenceposters/', include('djangoplicity.products.urls.conference_posters'), { 'model': Poster, 'options': ConferencePosterOptions } ),
    ( r'^extras/exhibitions/', include('djangoplicity.products.urls.exhibitions'), { 'model': Exhibition, 'options': ExhibitionOptions } ),
    ( r'^extras/stickers/', include('djangoplicity.products.urls.stickers'), { 'model': Sticker, 'options': StickerOptions } ),
    ( r'^extras/postcards/', include('djangoplicity.products.urls.postcards'), { 'model': PostCard, 'options': PostCardOptions } ),
    ( r'^extras/posters/', include('djangoplicity.products.urls.posters'), { 'model': Poster, 'options': PosterOptions } ),
    ( r'^extras/merchandise/', include('djangoplicity.products.urls.merchandise'), { 'model': Merchandise, 'options': MerchandiseOptions } ),
    ( r'^extras/dvds/', include('djangoplicity.products.urls.cdroms'), { 'model': CDROM, 'options': CDROMOptions } ),
	( r'^extras/slideshows/', include('djangoplicity.products.urls.slideshows'), { 'model': SlideShow, 'options': SlideShowOptions } ),
	#( r'^extras/printlayouts/', include('djangoplicity.products.urls.printlayouts'), { 'model': Release, 'options': PrintLayoutOptions } ),
	( r'^extras/presentations/', include('djangoplicity.products.urls.presentations'), { 'model': Presentation, 'options': PresentationOptions } ),
	( r'^kidsandteachers/education/', include('djangoplicity.products.urls.education'), { 'model': EducationalMaterial, 'options': EducationalMaterialOptions } ),
	( r'^kidsandteachers/drawings/', include('djangoplicity.products.urls.drawings'), { 'model': KidsDrawing, 'options': KidsDrawingOptions } ),
	( r'^press/kits/', include('djangoplicity.products.urls.presskits'), { 'model': PressKit, 'options': PressKitOptions } ),
	
    ( r'^projects/fits_liberator/fitsimages/', include('djangoplicity.products.urls.fitsimages'), { 'model': FITSImage, 'options': FITSImageOptions } ),
    
    
#    ( r'^rss/feed.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'feed.xml' } ),
#    ( r'^rss/vodcast.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'vodcast.xml' } ),
#    ( r'^rss/vodcastfullhd.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'vodcastfullhd.xml' } ),
#    ( r'^rss/vodcasthd.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'vodcasthd.xml' } ),
#    ( r'^rss/hubblecasthd_amp.xml$', 'spacetelescope.views.rssfeedhack', { 'rssfile': 'hubblecasthd_amp.xml' } ),
    ( r'^rss/feed.xml$', redirect_to, { 'url': 'http://feeds.feedburner.com/hubble_news/' } ),
    ( r'^rss/vodcast.xml$', redirect_to, { 'url': 'http://feeds.feedburner.com/hubblecast_sd/' } ),
    ( r'^rss/vodcasthd.xml$', redirect_to, { 'url': 'http://feeds.feedburner.com/hubblecast/' } ),
    ( r'^rss/vodcastfullhd.xml$', redirect_to, { 'url': 'http://feeds.feedburner.com/hubblecast_fullhd/' } ),
    ( r'^rss/hubblecasthd_amp.xml$', redirect_to, { 'url': 'http://feeds.feedburner.com/hubblecast/' } ),
    
    # User authentication
    ( r'^login/$', 'djangoplicity.authtkt.views.login', { 'template_name': 'login.html', 'SSL' : True } ),
 	( r'^logout/$', 'djangoplicity.authtkt.views.logout', { 'template_name': 'logout.html', 'SSL' : True } ),
 	( r'^password_reset/$', 'django.contrib.auth.views.password_reset', { 'SSL' : True, 'email_template_name' : 'registration/password_reset_email.txt' } ),
	( r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', { 'SSL' : True } ),
	( r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', { 'SSL' : True } ),
	( r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', { 'SSL' : True } ),
	
 	# Shop 
 	( r'^shop/terms/', redirect_to, { 'url': '/shop/terms_conditions/' }, 'shop_terms' ),
 	( r'^shop/ccv/', redirect_to, { 'url': '/shop/cvc_info/' }, 'shop_ccv' ),
 	( r'^shop/freeorder/$', include( 'djangoplicity.archives.contrib.satchmo.freeorder.urls' ) ),
 	( r'^shop/', include( 'djangoplicity.archives.contrib.satchmo.urls' ) ),
 	
 	# Google Webmaster Toolkit verification
 	( r'^', include( 'djangoplicity.google.urls' ) ), 

 	# Main view
 	( r'^$', 'spacetelescope.views.main_page' ),
 	
 	
 )

#handler404 = 'spacetelescope.views.page_not_found'

# Static files/media serving during development
if settings.SERVE_STATIC_MEDIA:
    urlpatterns += patterns( '',
        ( r'^' + settings.STATIC_MEDIA_PREFIX + r'/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True } ),
				)
