from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client


class TestInitial(TestCase):
    def setUp(self):
        self.user = AnonymousUser()
        self.client = Client()

    def test_frontpage_with_client(self):
        """"
        In order to use django.test.Client we need to ensure the Authentication and Session
        middlewares to be loaded previous to the djangoplicity middleware, because the latter
        requires access to request.user which is added by AuthenticationMiddleware which,
        in turn requires SessionMiddleware
        """
        response = self.client.get('/')
        self.assertContains(response, '<div id="pr-carousel">', status_code=200, html=True)
