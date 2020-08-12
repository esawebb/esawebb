# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
import json
from django.test import TestCase, Client
from djangoplicity.media.models import Video


def load_json(response):
    return json.loads(response.content)


class TestFrontPageApp(TestCase):
    fixtures = ['test']

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

    def test_d2d_view(self):
        response = self.client.get('/d2d/')

        json_response = load_json(response)

        self.assertIn('Creator', json_response)
        self.assertIn('URL', json_response)

        self.assertEqual('ESA/Hubble', json_response.get('Creator'))
        self.assertEqual('https://www.spacetelescope.org', json_response.get('URL'))
