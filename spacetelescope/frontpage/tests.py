# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
from django.test import TestCase, Client, tag
from djangoplicity.media.models import Video


@tag('frontpage')
class TestFrontPageApp(TestCase):
    fixtures = ['test/pages', 'test/media', 'test/announcements', 'test/releases', 'test/highlights']

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        youtube_only_html = '<div class="youtube-wrapper"><div id="youtube-player"></div></div>'

        # first hubblecast with use_youtube = True
        response = self.client.get('/')

        self.assertContains(response, 'Announcements')
        self.assertContains(response, youtube_only_html, html=True)

        # first hubblecast with use_youtube = False
        Video.objects.update(use_youtube=False)
        response = self.client.get('/')

        self.assertNotContains(response, youtube_only_html, html=True)
