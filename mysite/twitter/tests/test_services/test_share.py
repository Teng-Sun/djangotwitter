from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from twitter.views.services import share


class ShareTest(TestCase):

    def test_search_username(self):
        data = [
            ('#hello', []),
            ('@#hello', []),
            ('@h#ello', ['h']),
            ('tweet content', []),
            ('@hello tweet content', ['hello']),
            ('tweet @hello content', ['hello']),
            ('tweet@hello content', ['hello']),
            ('@hello @world tweet content', ['hello', 'world']),
            ('@hello tweet @world content', ['hello', 'world'])
        ]
        for content, username_should_be in data:
            username = share.search_username(content)
            self.assertEquals(username, username_should_be)



            
            
        







