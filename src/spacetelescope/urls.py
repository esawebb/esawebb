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
from spacetelescope import listener


from djangoplicity.announcements.models import Announcement, WebUpdate
from djangoplicity.announcements.options import AnnouncementOptions, WebUpdateOptions
from djangoplicity.media.models import Image, Video, PictureOfTheWeek, ImageComparison
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions, ImageComparisonOptions
from django.views.generic.simple import redirect_to

from djangoplicity.products.models import *
from djangoplicity.products.options import *

from djangoplicity.releases.models import Release
from djangoplicity.releases.options import ReleaseOptions

from djangoplicity.newsletters.models import Newsletter
from djangoplicity.newsletters.options import NewsletterOptions

from djangoplicity.science.models import ScienceAnnouncement
from djangoplicity.science.options import ScienceAnnouncementOptions

#from djangoplicity.events.models import Event
#from djangoplicity.events.options import EventOptions

from satchmo_store.urls import basepatterns
from shipping.urls import adminpatterns

urlpatterns = []

urlpatterns += patterns( '',

    # Djangoplicity Adminstration
    ( r'^admin/cache/', include( 'djangoplicity.cache.urls', namespace="admincache_site", app_name="cache" ), { 'SSL': True } ),
    ( r'^admin/history/', include( 'djangoplicity.adminhistory.urls', namespace="adminhistory_site", app_name="history" ), { 'SSL': True } ),
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ), { 'SSL': True } ),
    ( r'^admin/menus/', include( 'djangoplicity.menus.urls' ), { 'SSL' : True } ),
    ( r'^admin(.*)({{\s?MEDIA_URL\s?}})(?P<path>.*)', 'djangoplicity.views.adm_translate_static_media_path', { 'SSL' : True } ),
#    ( r'^admin/shop/shop/order/(?P<order_id>[0-9]+)/csv/', 'djangoplicity.coposweb.views.order_csv_file', { 'SSL': True } ),
	( r'^admin/shop/', include( 'djangoplicity.archives.contrib.satchmo.urls_admin' ), { 'SSL': True } ),
	( r'^admin/shop/', include(adminshop_site.urls), { 'SSL': True, 'extra_context' : { 'ADMINSHOP_SITE' : True } } ),
	( r'^admin/system/', include(adminlogs_site.urls), { 'SSL': True, 'extra_context' : { 'ADMINLOGS_SITE' : True }  } ),
	( r'^admin/', include(admin_site.urls), { 'SSL': True, 'extra_context' : { 'ADMIN_SITE' : True }  } ),
	( r'^admin/import/', include('djangoplicity.archives.importer.urls'), { 'SSL': True } ),
	( r'^tinymce/', include('tinymce.urls'), { 'SSLAllow': True } ),

    # Server alive check (used for load balancers - called every 5 secs )
    ( r'^alive-check.dat$', 'djangoplicity.views.alive_check', { 'SSLAllow' : True } ),
    ( r'^sitemap/', 'djangoplicity.menus.views.sitemap' ),

    # Media Archive
    ( r'^images/potw/', include('djangoplicity.media.urls_potw'), { 'model': PictureOfTheWeek, 'options': PictureOfTheWeekOptions } ),
    ( r'^images/comparisons/', include('djangoplicity.media.urls_imagecomparisons'), { 'model': ImageComparison, 'options': ImageComparisonOptions } ),
	( r'^images/', include('djangoplicity.media.urls_images'), { 'model': Image, 'options': ImageOptions } ),
    #( r'^news/feed/(?P<url>.*)/?$', 'django.contrib.syndication.views.feed', { 'feed_dict': ReleaseOptions.get_feeds() } ),
    ( r'^news/', include('djangoplicity.releases.urls'), { 'model': Release, 'options': ReleaseOptions } ),
    ( r'^videos/uservideos/', include('djangoplicity.products.urls.uservideos'), { 'model': UserVideo, 'options': UserVideoOptions } ),
    ( r'^videos/', include('djangoplicity.media.urls_videos'), { 'model': Video, 'options': VideoOptions } ),

	# Other archives
	( r'^announcements/webupdates/', include('djangoplicity.announcements.urls_webupdates'), { 'model': WebUpdate, 'options': WebUpdateOptions } ),
    ( r'^announcements/', include('djangoplicity.announcements.urls'), { 'model': Announcement, 'options': AnnouncementOptions } ),
    ( r'^about/further_information/books/', include('djangoplicity.products.urls.books'), { 'model': Book, 'options': BookOptions } ),
    ( r'^about/further_information/brochures/', include('djangoplicity.products.urls.brochures'), { 'model': Brochure, 'options': BrochureOptions } ),
    ( r'^about/further_information/flyers/', include('djangoplicity.products.urls.flyers'), { 'model': Flyer, 'options': FlyerOptions } ),
    ( r'^about/further_information/handouts/', include('djangoplicity.products.urls.handouts'), { 'model': Handout, 'options': HandoutOptions } ),
    ( r'^about/further_information/maps/', include('djangoplicity.products.urls.maps'), { 'model': Map, 'options': MapOptions } ),
    ( r'^about/further_information/messengers/', include('djangoplicity.products.urls.messengers'), { 'model': Messenger, 'options': MessengerOptions } ),
	( r'^about/further_information/newsletters/', include('djangoplicity.products.urls.periodicals'), { 'model': Periodical, 'options': PeriodicalOptions } ),
    ( r'^about/further_information/schools/', include('djangoplicity.products.urls.schools'), { 'model': ScienceInSchool, 'options': ScienceInSchoolOptions } ),
    ( r'^about/further_information/capjournals/', include('djangoplicity.products.urls.capjournals'), { 'model': CapJournal, 'options': CapJournalOptions } ),
    ( r'^about/further_information/stecfnewsletters/', include('djangoplicity.products.urls.stecfnewsletters'), { 'model': STECFNewsletter, 'options': STECFNewsletterOptions } ),
    ( r'^about/further_information/bulletins/', include('djangoplicity.products.urls.bulletins'), { 'model': Bulletin, 'options': BulletinOptions } ),
    ( r'^about/further_information/techdocs/', include('djangoplicity.products.urls.techdocs'), { 'model': TechnicalDocument, 'options': TechnicalDocumentOptions } ),
	( r'^extras/calendars/', include('djangoplicity.products.urls.calendars'), { 'model': Calendar, 'options': CalendarOptions } ),
	( r'^extras/applications/', include('djangoplicity.products.urls.applications'), { 'model': Application, 'options': ApplicationOptions } ),
    ( r'^extras/art/', include('djangoplicity.products.urls.art'), { 'model': OnlineArt, 'options': OnlineArtOptions } ),
	( r'^extras/artists/', include('djangoplicity.products.urls.artists'), { 'model': OnlineArtAuthor, 'options': OnlineArtAuthorOptions } ),
    ( r'^extras/logos/', include('djangoplicity.products.urls.logos'), { 'model': Logo, 'options': LogoOptions } ),
    #( r'^extras/conferenceposters/', include('djangoplicity.products.urls.conference_posters'), { 'model': Poster, 'options': ConferencePosterOptions } ),
    ( r'^extras/exhibitions/', include('djangoplicity.products.urls.exhibitions'), { 'model': Exhibition, 'options': ExhibitionOptions } ),
    ( r'^extras/stickers/', include('djangoplicity.products.urls.stickers'), { 'model': Sticker, 'options': StickerOptions } ),
    ( r'^extras/postcards/', include('djangoplicity.products.urls.postcards'), { 'model': PostCard, 'options': PostCardOptions } ),
    ( r'^extras/print_posters/', include('djangoplicity.products.urls.print_posters'), { 'model': PrintedPoster, 'options': PrintedPosterOptions } ),
    ( r'^extras/conf_posters/', include('djangoplicity.products.urls.conf_posters'), { 'model': ConferencePoster, 'options': ConferencePosterOptions } ),
    ( r'^extras/elec_posters/', include('djangoplicity.products.urls.elec_posters'), { 'model': ElectronicPoster, 'options': ElectronicPosterOptions } ),
    ( r'^extras/apparel/', include('djangoplicity.products.urls.apparels'), { 'model': Apparel, 'options': ApparelOptions } ),
    ( r'^extras/merchandise/', include('djangoplicity.products.urls.merchandise'), { 'model': Merchandise, 'options': MerchandiseOptions } ),
    ( r'^extras/media/', include('djangoplicity.products.urls.cdroms'), { 'model': CDROM, 'options': CDROMOptions } ),
	( r'^extras/slideshows/', include('djangoplicity.products.urls.slideshows'), { 'model': SlideShow, 'options': SlideShowOptions } ),
	( r'^extras/imaxfilms/', include('djangoplicity.products.urls.imaxfilms'), { 'model': IMAXFilm, 'options': IMAXFilmOptions } ),
	#( r'^extras/printlayouts/', include('djangoplicity.products.urls.printlayouts'), { 'model': Release, 'options': PrintLayoutOptions } ),
	( r'^extras/presentations/', include('djangoplicity.products.urls.presentations'), { 'model': Presentation, 'options': PresentationOptions } ),
	( r'^kidsandteachers/education/', include('djangoplicity.products.urls.education'), { 'model': EducationalMaterial, 'options': EducationalMaterialOptions } ),
	( r'^kidsandteachers/drawings/', include('djangoplicity.products.urls.drawings'), { 'model': KidsDrawing, 'options': KidsDrawingOptions } ),
	( r'^press/kits/', include('djangoplicity.products.urls.presskits'), { 'model': PressKit, 'options': PressKitOptions } ),
	( r'^forscientists/announcements/', include('djangoplicity.science.urls'), { 'model': ScienceAnnouncement, 'options': ScienceAnnouncementOptions } ),

    ( r'^projects/fits_liberator/fitsimages/', include('djangoplicity.products.urls.fitsimages'), { 'model': FITSImage, 'options': FITSImageOptions } ),

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
 	( r'^shop/bulkorders/', redirect_to, { 'url': '/shop/bulk_orders/' }, 'shop_bulkorders' ),
 	( r'^shop/freeorder/$', include( 'djangoplicity.archives.contrib.satchmo.freeorder.urls' ) ),
 	( r'^shop/', include( 'djangoplicity.archives.contrib.satchmo.urls' ) ),
 	( r'^newsletters/', include( 'djangoplicity.mailinglists.urls', namespace='djangoplicity_mailinglists', app_name='djangoplicity_mailinglists' ), { 'SSLAllow' : True } ),
	( r'^newsletters/', include( 'djangoplicity.newsletters.urls'), { 'model': Newsletter, 'options': NewsletterOptions, } ),
	#( r'^public/djangoplicity/events/', include('djangoplicity.events.urls'), { 'model': Event, 'options': EventOptions } ),
	( r'^facebook/', include('djangoplicity.iframe.urls'), { 'SSLAllow' : True }  ),

 	# Google Webmaster Toolkit verification
 	( r'^', include( 'djangoplicity.google.urls' ) ),

	# Image votes
	( r'^projects/hiddentreasures/vote/', include('djangoplicity.imgvote.urls'), ),

 	# Main view
 	( r'^$', 'spacetelescope.views.main_page' ),


 )

#handler404 = 'spacetelescope.views.page_not_found'

# Static files/media serving during development
if settings.SERVE_STATIC_MEDIA:
    urlpatterns += patterns( '',
		( r'^' + settings.DJANGOPLICITY_MEDIA_URL[1:] + r'(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DJANGOPLICITY_MEDIA_ROOT, 'show_indexes': True } ),
		( r'^' + settings.MEDIA_URL[1:] + r'(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True } ),
	)
