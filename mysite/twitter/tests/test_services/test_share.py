from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.test import Client

from twitter.views.services import share


class ShareTest(TestCase):


    def test_pagination(self):
        c = Client()
        response = c.get('/profile/admin')
        request = response.wsgi_request
        object_list = [
            1, 2, 3, 4, 5, 6, 7
        ]

        data = [
            (3, True),
            (7, False)
        ]
        for item, show in data:
            text, show_should = share.pagination(request, object_list, item)
            self.assertEqual(show_should, show)