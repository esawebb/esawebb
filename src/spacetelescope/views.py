# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from djangoplicity.announcements.models import Announcement
from djangoplicity.media.models import Image, Video, PictureOfTheWeek
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions
from djangoplicity.releases.models import Release


@cache_page( 60 * 5 )
def frontpage( request ):
	""" Front page """

	hubblecasts = VideoOptions.Queries.category.queryset( Video, VideoOptions, request, stringparam='hubblecast' )[0].order_by('-release_date', )[:5]

	return render_to_response('frontpage.html', {
		'releases': Release.get_latest_release( 5 ),
		'potws': PictureOfTheWeekOptions.Queries.default.queryset( PictureOfTheWeek, PictureOfTheWeekOptions, request )[0][:10],
		'announcements': Announcement.get_latest_announcement(5, only_featured=True),
		'hubblecasts': hubblecasts,
		'top100': ImageOptions.Queries.top100.queryset( Image, ImageOptions, request )[0][:20],
	}, context_instance=RequestContext(request) )


def shop_closed( request ):
	""" Main Page view """
	return render_to_response( 'shop_closed.html', {}, context_instance=RequestContext( request ) )
