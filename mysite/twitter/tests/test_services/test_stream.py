from django.contrib.auth.models import User
from django.test import TestCase

from twitter.models import Tweet, Stream
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

        self.tweet_a = Tweet.objects.get(pk=1)
        self.tweet_1 = Tweet.objects.get(pk=2)
        self.tweet_2 = Tweet.objects.get(pk=3)

        self.reply_a_r_a = Tweet.objects.get(pk=7)
        self.reply_a_r_1 = Tweet.objects.get(pk=9)
        self.reply_a_r_2 = Tweet.objects.get(pk=13)

        self.retweet_a_re_1 = Tweet.objects.get(pk=12)


    def test_is_receiver(self):
        data = [
            (self.tweet_a,[self.user1, self.user2], [True, True]),
            (self.tweet_1, [self.user2], [True]),
            (self.reply_a_r_a, [self.user1, self.user2], [True, True]),
            (self.reply_a_r_1, [self.user1, self.user2], [True, True]),
            (self.reply_a_r_2, [self.user1, self.user2], [False, True]),
            (self.retweet_a_re_1, [self.user1, self.user2], [True, True])
        ]

        for tweet, followers, results in data:
            for index, follower in enumerate(followers):
                is_receiver_result = stream.is_receiver(tweet, follower)
                self.assertEquals(results[index], is_receiver_result)

    def test_get_receivers(self):
        data = [
            (self.tweet_a, set([self.admin, self.user1, self.user2])),
            (self.tweet_1, set([self.user1, self.user2])),
            (self.tweet_2, set([self.user2])),
            (self.reply_a_r_a, set([self.admin, self.user1, self.user2])),
            (self.reply_a_r_1, set([self.admin, self.user1, self.user2])),
            (self.reply_a_r_2, set([self.admin, self.user2])),
            (self.retweet_a_re_1, set([self.admin, self.user1, self.user2]))
        ]
        for tweet, receivers_should_be in data:
            receivers = stream.get_receivers(tweet)
            self.assertEquals(receivers, receivers_should_be)

    def test_create_streams(self):
        data = [
            (self.tweet_a, Stream.TWEET),
            (self.reply_a_r_a, Stream.REPLY),
            (self.retweet_a_re_1, Stream.RETWEET)
        ]
        for tweet, stream_type in data:
            stream.create_streams(tweet, stream_type)
            stream_list = Stream.objects.filter(tweet=tweet)
            receivers = stream.get_receivers(tweet)
            for stream_item in stream_list:
                self.assertEquals(stream_item.tweet, tweet)
                self.assertEquals(stream_item.stream_type, stream_type)
                self.assertIn(stream_item.receiver, receivers)