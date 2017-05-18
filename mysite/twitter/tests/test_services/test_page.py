from django.contrib.auth.models import User
from django.contrib.auth import login
from django.test import TestCase, Client

from twitter.models import Stream
from twitter.views.services import page

class PageTest(TestCase):
    fixtures = [
        'twitter/fixtures/test_user_data.json',
        'twitter/fixtures/test_stream_data.json',
        'twitter/fixtures/test_tweet_data.json'
    ]

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')

        self.c = Client()

        self.stream_1 = Stream.objects.get(pk=1)
        self.stream_2 = Stream.objects.get(pk=2)


    def test_index(self):
        response = self.c.get('index')
        request = response.wsgi_request
        login(request, self.admin)
        render_data = page.index(request)
        streams = render_data['stream_list']
        self.assertEqual(streams, render_data['object_list'])
        for s in streams:
            self.assertEqual(s.tweet, self.stream_1.tweet)
        self.assertEqual(render_data['show_pagination'], False)