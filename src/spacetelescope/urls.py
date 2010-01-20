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
from spacetelescope.admin import admin_site, adminlogs_site


from djangoplicity.media.models import Image, Video
from djangoplicity.media.options import ImageOptions, VideoOptions
from django.views.generic.simple import redirect_to

from djangoplicity.releases.models import Release
from djangoplicity.releases.options import ReleaseOptions


urlpatterns = patterns( '',    
    # Djangoplicity Adminstration 
    ( r'^admin/cache/', include( 'djangoplicity.cache.urls', namespace="admincache_site", app_name="cache" ), { 'SSL': True } ),
    ( r'^admin/log/', include( 'djangoplicity.contrib.admin.log.urls', namespace="adminhistory_site", app_name="history" ), { 'SSL': True } ),
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ), { 'SSL': True } ),
    ( r'^admin(.*)({{\s?MEDIA_URL\s?}})(?P<path>.*)', 'djangoplicity.views.adm_translate_static_media_path', { 'SSL' : True } ),
	( r'^admin/system/', include(adminlogs_site.urls), { 'SSL': True } ),
	( r'^admin/', include(admin_site.urls), { 'SSL': True } ),
	( r'^admin/import/', include('djangoplicity.archives.importer.urls'), { 'SSL': True } ),
	 
    # Server alive check (used for load balancers - called every 5 secs )
    ( r'^alive-check.dat$', 'djangoplicity.views.alive_check', { 'SSLAllow' : True } ),

    ( r'^images/', include('djangoplicity.media.urls_images'), { 'model': Image, 'options': ImageOptions } ),
    ( r'^news/feed/(?P<url>.*)/?$', 'django.contrib.syndication.views.feed', { 'feed_dict': ReleaseOptions.feeds } ),
    ( r'^news/', include('djangoplicity.releases.urls'), { 'model': Release, 'options': ReleaseOptions } ),
    ( r'^videos/', include('djangoplicity.media.urls_videos'), { 'model': Video, 'options': VideoOptions } ),
    
    # User authentication
    ( r'^login/$', 'djangoplicity.authtkt.views.login', { 'template_name': 'login.html', 'SSL' : True } ),
 	( r'^logout/$', 'djangoplicity.authtkt.views.logout', { 'template_name': 'logout.html', 'SSL' : True } ),
 	
 	# Main view
 	( r'^$', 'spacetelescope.views.main_page' ),
 )

#handler404 = 'spacetelescope.views.page_not_found'


# Static files/media serving during development
if settings.SERVE_STATIC_MEDIA:
    urlpatterns += patterns( '',
        ( r'^' + settings.STATIC_MEDIA_PREFIX + r'/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT } ),
				)
