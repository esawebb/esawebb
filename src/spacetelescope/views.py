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
from djangoplicity.media.options import ImageOptions, VideoOptions
from djangoplicity.releases.models import Release


@cache_page( 60 * 5 )
def frontpage( request ):
	""" Front page """

	from datetime import datetime
	now = datetime.now()
	potd = ImageOptions.Queries.default.queryset( Image, ImageOptions, request )[0][now.day]
	votd = VideoOptions.Queries.default.queryset( Video, VideoOptions, request )[0][now.day]
	hubblecasts = VideoOptions.Queries.category.queryset( Video, VideoOptions, request, stringparam='hubblecast' )[0].order_by('-release_date', )[:5]

	return render_to_response('frontpage.html', {
		'releases': Release.get_latest_release( 5 ),
		'potw': PictureOfTheWeek.get_latest(),
		'announcements': Announcement.get_latest_announcement(5, only_featured=True),
		'hubblecasts': hubblecasts,
		'potd': potd,
		'votd': votd,
		#'announcements': Announcement.get_latest_release( settings.FRONTPAGE_PRESSRELEASES_LEN ),
	}, context_instance=RequestContext(request) )


def shop_closed( request ):
	""" Main Page view """
	return render_to_response( 'shop_closed.html', {}, context_instance=RequestContext( request ) )
