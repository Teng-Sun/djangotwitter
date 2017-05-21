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
            (3, 3),
            (7, 1)
        ]

        for by, num in data:
            text = share.pagination(request, object_list, by)
            self.assertEqual(text.paginator.num_pages, num)