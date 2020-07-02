# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
import unittest

from models import Highlight
from django.db import models
from django.test import RequestFactory, TestCase

from collections import OrderedDict

from django.http import JsonResponse
from django.views.generic.base import TemplateView

from djangoplicity.announcements.models import Announcement
from djangoplicity.media.models import Image, Video, PictureOfTheWeek
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions
from djangoplicity.releases.models import Release

from django.contrib.auth.models import User
from views import FrontpageView

class HighlightModelTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		#Set up non-modified objects used by all test methods
		Highlight.objects.create(name='/page42/', title='Pagefortest', description='This is a Page for test', image='Thisisaimage', link ='link/page/image', order = '1', published = 'False')

	def test_first_name_label(self):
		highlight=Highlight.objects.get(id=1)
		field_label = highlight._meta.get_field('name').verbose_name
		self.assertEquals(field_label,'name')

	def test_first_title_label(self):
		highlight=Highlight.objects.get(id=1)
		field_label = highlight._meta.get_field('title').verbose_name
		self.assertEquals(field_label,'title')

	def test_first_description_label(self):
		highlight=Highlight.objects.get(id=1)
		field_label = highlight._meta.get_field('description').verbose_name
		self.assertEquals(field_label,'description')

	def test_first_image_label(self):
		highlight=Highlight.objects.get(id=1)
		field_label = highlight._meta.get_field('image').verbose_name
		self.assertEquals(field_label,'image')

	def test_first_link_label(self):
		highlight=Highlight.objects.get(id=1)
		field_label = highlight._meta.get_field('link').verbose_name
		self.assertEquals(field_label,'link')

	def test_first_order_label(self):
		highlight=Highlight.objects.get(id=1)
		field_label = highlight._meta.get_field('order').verbose_name
		self.assertEquals(field_label,'order')

	def test_first_published_label(self):
		highlight=Highlight.objects.get(id=1)
		field_label = highlight._meta.get_field('published').verbose_name
		self.assertEquals(field_label,'published')

	def test_title_max_length(self):
		highlight=Highlight.objects.get(id=1)
		max_length = highlight._meta.get_field('title').max_length
		self.assertEquals(max_length,255)

	def test_image_max_length(self):
		highlight=Highlight.objects.get(id=1)
		max_length = highlight._meta.get_field('image').max_length
		self.assertEquals(max_length,255)

	def test_link_max_length(self):
		highlight=Highlight.objects.get(id=1)
		max_length = highlight._meta.get_field('link').max_length
		self.assertEquals(max_length,255)

	def test_unicode(self):
		highlight=Highlight.objects.get(id=1)
		self.assertEquals("/page42/",unicode(highlight))

class FrontpageViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='test', password='test')
		self.rf = RequestFactory()

	def test_announcements_set_in_context(self):
		request = self.rf.get('/')
		request.user = self.user
		response = FrontpageView.as_view()(request)
		self.assertEquals(response.status_code,200)
