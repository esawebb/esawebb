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


from djangoplicity.media.models import Image, Video
from djangoplicity.media.options import ImageOptions, VideoOptions
from django.views.generic.simple import redirect_to

from djangoplicity.releases.models import Release
from djangoplicity.releases.options import ReleaseOptions

from spacetelescope.archives.educational.models import *
from spacetelescope.archives.educational.options import *
from spacetelescope.archives.goodies.models import *
from spacetelescope.archives.goodies.options import *
from spacetelescope.archives.products.models import *
from spacetelescope.archives.products.options import *
from spacetelescope.archives.projects.models import *
from spacetelescope.archives.projects.options import *
from spacetelescope.archives.org.models import *
from spacetelescope.archives.org.options import *

from satchmo_store.urls import basepatterns

urlpatterns = []

urlpatterns += basepatterns + patterns( '',    
    # Djangoplicity Adminstration 
    ( r'^admin/cache/', include( 'djangoplicity.cache.urls', namespace="admincache_site", app_name="cache" ), { 'SSL': True } ),
    ( r'^admin/log/', include( 'djangoplicity.contrib.admin.log.urls', namespace="adminhistory_site", app_name="history" ), { 'SSL': True } ),
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ), { 'SSL': True } ),
    ( r'^admin(.*)({{\s?MEDIA_URL\s?}})(?P<path>.*)', 'djangoplicity.views.adm_translate_static_media_path', { 'SSL' : True } ),
	( r'^admin/shop/', include(adminshop_site.urls), { 'SSL': True } ),
	( r'^admin/system/', include(adminlogs_site.urls), { 'SSL': True } ),
	( r'^admin/', include(admin_site.urls), { 'SSL': True } ),
	( r'^admin/import/', include('djangoplicity.archives.importer.urls'), { 'SSL': True } ),
	
	 
    # Server alive check (used for load balancers - called every 5 secs )
    ( r'^alive-check.dat$', 'djangoplicity.views.alive_check', { 'SSLAllow' : True } ),
    ( r'^sitemap/', 'djangoplicity.menus.views.sitemap' ),

    ( r'^images/', include('djangoplicity.media.urls_images'), { 'model': Image, 'options': ImageOptions } ),
    #( r'^news/feed/(?P<url>.*)/?$', 'django.contrib.syndication.views.feed', { 'feed_dict': ReleaseOptions.feeds } ),
    ( r'^news/', include('djangoplicity.releases.urls'), { 'model': Release, 'options': ReleaseOptions } ),
    ( r'^videos/', include('djangoplicity.media.urls_videos'), { 'model': Video, 'options': VideoOptions } ),

    # Education
    ( r'^kidsandteachers/education/', include('spacetelescope.archives.educational.urls.education'), { 'model': EducationalMaterial, 'options': EducationalMaterialOptions } ),
    ( r'^kidsandteachers/drawings/', include('spacetelescope.archives.educational.urls.drawings'), { 'model': KidsDrawing, 'options': KidsDrawingOptions } ),

    # Goodies
    ( r'^extras/calendars/', include('spacetelescope.archives.goodies.urls.calendars'), { 'model': Calendar, 'options': CalendarOptions } ),
    ( r'^extras/art/', include('spacetelescope.archives.goodies.urls.art'), { 'model': OnlineArt, 'options': OnlineArtOptions } ),
    ( r'^extras/artists/', include('spacetelescope.archives.goodies.urls.artists'), { 'model': OnlineArtAuthor, 'options': OnlineArtAuthorOptions } ),
    
    # TODO: assess if we can handle print layouts with Release Archive, but just different options
    #( r'^goodies/printlayouts/', include('spacetelescope.archives.goodies.urls.printlayouts'), { 'model': Release, 'options': PrintLayoutOptions } ),
    
    ( r'^extras/presentations/', include('spacetelescope.archives.goodies.urls.slideshows'), { 'model': SlideShow, 'options': SlideShowOptions } ),


    #TODO: map to ST?
    # PRODUCTS
    ( r'^extras/dvds/', include('spacetelescope.archives.products.urls.cdroms'), { 'model': CDROM, 'options': CDROMOptions } ),
    ( r'^about/further_information/books/', include('spacetelescope.archives.products.urls.books'), { 'model': Book, 'options': BookOptions } ),
    ( r'^about/further_information/brochures/', include('spacetelescope.archives.products.urls.brochures'), { 'model': Brochure, 'options': BrochureOptions } ),
    ( r'^extras/merchandise/', include('spacetelescope.archives.products.urls.merchandise'), { 'model': Merchandise, 'options': MerchandiseOptions } ),
    ( r'^about/further_information/newsletters/', include('spacetelescope.archives.products.urls.newsletters'), { 'model': Newsletter, 'options': NewsletterOptions } ),
    ( r'^extras/postcards/', include('spacetelescope.archives.products.urls.postcards'), { 'model': PostCard, 'options': PostCardOptions } ),
    ( r'^extras/posters/', include('spacetelescope.archives.products.urls.posters'), { 'model': Poster, 'options': PosterOptions } ),
    ( r'^press/kits/', include('spacetelescope.archives.products.urls.presskits'), { 'model': PressKit, 'options': PressKitOptions } ),
    ( r'^extras/stickers/', include('spacetelescope.archives.products.urls.stickers'), { 'model': Sticker, 'options': StickerOptions } ),
    
    
    # ORG
    #TODO: is "announcements" gonna be the new prefix?
    ( r'^announcements/', include('spacetelescope.archives.org.urls.announcements'), { 'model': Announcement, 'options': AnnouncementOptions } ),
    ( r'^about/further_information/techdocs/', include('spacetelescope.archives.org.urls.techdocs'), { 'model': TechnicalDocument, 'options': TechnicalDocumentOptions } ),
    ( r'^extras/logos/', include('spacetelescope.archives.org.urls.logos'), { 'model': Logo, 'options': LogoOptions } ),
    ( r'^extras/conferenceposters/', include('spacetelescope.archives.org.urls.conference_posters'), { 'model': ConferencePoster, 'options': ConferencePosterOptions } ),
    
    # Projects
    ( r'^extras/exhibitions/', include('spacetelescope.archives.projects.urls.exhibitions'), { 'model': Exhibition, 'options': ExhibitionOptions } ),
    ( r'^projects/fits_liberator/fitsimages/', include('spacetelescope.archives.projects.urls.fitsimages'), { 'model': FITSImage, 'options': FITSImageOptions } ),
    
    # User authentication
    ( r'^login/$', 'djangoplicity.authtkt.views.login', { 'template_name': 'login.html', 'SSL' : True } ),
 	( r'^logout/$', 'djangoplicity.authtkt.views.logout', { 'template_name': 'logout.html', 'SSL' : True } ),
 	
 	# Main view
 	( r'^$', 'spacetelescope.views.main_page' ),
 )

urlpatterns += basepatterns + patterns('',
        (r'^shop/', include('satchmo_store.shop.urls')),
    )

#handler404 = 'spacetelescope.views.page_not_found'


# Static files/media serving during development
if settings.SERVE_STATIC_MEDIA:
    urlpatterns += patterns( '',
        ( r'^' + settings.STATIC_MEDIA_PREFIX + r'/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True } ),
				)
