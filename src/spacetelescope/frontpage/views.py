# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010-2015 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>

from django.views.generic.base import TemplateView
from djangoplicity.announcements.models import Announcement
from djangoplicity.media.models import Image, Video, PictureOfTheWeek
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions
from djangoplicity.releases.models import Release

from spacetelescope.frontpage.models import Highlight


class FrontpageView(TemplateView):

	template_name = 'frontpage.html'

	def get_context_data(self, **kwargs):
		context = super(FrontpageView, self).get_context_data(**kwargs)

		context['announcements'] = Announcement.get_latest_announcement(20, only_featured=True)
		context['highlights'] = Highlight.objects.filter(published=True)
		context['hubblecasts'] = VideoOptions.Queries.category.queryset(Video, VideoOptions, self.request, stringparam='hubblecast')[0].order_by('-release_date',)[:10]
		context['potws'] = PictureOfTheWeekOptions.Queries.default.queryset(PictureOfTheWeek, PictureOfTheWeekOptions, self.request)[0][:10]
		context['releases'] = Release.get_latest_release(5)
		context['top100'] = ImageOptions.Queries.top100.queryset(Image, ImageOptions, self.request)[0][:20]

		return context
