from django.contrib.auth.models import User
from django.test import TestCase

from twitter.models import Tweet
from twitter.views.services import stream

class StreamTest(TestCase):
    fixtures = [
        'twitter/fixtures/test_user_data.json',
        'twitter/fixtures/test_tweet_data.json',
        'twitter/fixtures/test_followship_data.json',
        'twitter/fixtures/test_replyship_data.json',
    ]

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')

        self.tweet_from_admin = Tweet.objects.get(pk=1)
        self.tweet_from_user1 = Tweet.objects.get(pk=2)
        self.tweet_from_user2 = Tweet.objects.get(pk=3)
        self.reply_from_admin_to_admin = Tweet.objects.get(pk=5)
        self.reply_from_admin_to_user1 = Tweet.objects.get(pk=6)
        self.reply_from_admin_to_user2 = Tweet.objects.get(pk=7)
        self.reply_from_admin_to_user3 = Tweet.objects.get(pk=8)
        self.retweet_from_admin_to_admin = Tweet.objects.get(pk=9)

    def test_is_receiver(self):
        data = [
            (self.tweet_from_admin, [self.user1, self.user2], [True, True]),
            (self.tweet_from_user1, [self.user2], [True]),
            (self.reply_from_admin_to_admin, [self.user1, self.user2], [True, True]),
            (self.reply_from_admin_to_user1, [self.user1, self.user2], [True, True]),
            (self.reply_from_admin_to_user2, [self.user1, self.user2], [False, True]),
            (self.reply_from_admin_to_user3, [self.user1, self.user2], [False, False]),
            (self.retweet_from_admin_to_admin, [self.user1, self.user2], [True, True])
        ]

        for tweet, followers, results in data:
            for index, follower in enumerate(followers):
                is_receiver_result = stream.is_receiver(tweet, follower)
                self.assertEquals(results[index], is_receiver_result)