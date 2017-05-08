from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.test import Client

from twitter.views import handler
from twitter.models import Tweet, Stream

class HandleTest(TestCase):
    fixtures = [
        'twitter/fixtures/test_user_data.json',
        'twitter/fixtures/test_tweet_data.json',
        'twitter/fixtures/test_replyship_data.json',
        'twitter/fixtures/test_followship_data.json',
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




    def test_get_receivers_should_be_adminuser12_stream_type_tweet(self):
        users = set([self.admin, self.user1, self.user2])
        receivers = handler.get_receivers(self.tweet_from_admin, 'T')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_user12_stream_type_tweet(self):
        users = set([self.user1, self.user2])
        receivers = handler.get_receivers(self.tweet_from_user1, 'T')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_user2_stream_type_tweet(self):
        users = set([self.user2])
        receivers = handler.get_receivers(self.tweet_from_user2, 'T')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_admin_stream_type_reply(self):
        users = set([self.admin])
        receivers = handler.get_receivers(self.reply_from_admin_to_admin, 'Y')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_adminuser12_stream_type_reply(self):
        users = set([self.admin, self.user1, self.user2])
        receivers = handler.get_receivers(self.reply_from_admin_to_user1, 'Y')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_adminuser2_stream_type_reply(self):
        users = set([self.admin, self.user2])
        receivers = handler.get_receivers(self.reply_from_admin_to_user2, 'Y')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_admin_stream_type_reply(self):
        users = set([self.admin])
        receivers = handler.get_receivers(self.reply_from_admin_to_user3, 'Y')
        self.assertEqual(receivers, users)


    def test_check_followship_should_admin_not_follow_user1(self):
        followship = handler.check_followship(self.admin, self.user1)
        self.assertEqual(followship, False)

    def test_check_followship_should_user1_follows_admin(self):
        followship = handler.check_followship(self.user1, self.admin)
        self.assertEqual(followship, True)


    def test_create_streams(self):
        tweet = self.tweet_from_admin
        receivers = [self.admin, self.user1, self.user2]
        handler.create_streams(tweet, 'T')
        streams = Stream.objects.filter(tweet=tweet)
        for stream in streams:
            self.assertEqual(tweet, stream.tweet)
            self.assertEqual(stream.stream_type, 'T')
            self.assertIn(stream.receiver, receivers)



    def test_search_username_begin_with_shape(self):
        content = '#hello'
        username_should_be = []
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)

    def test_search_username_with_sharp(self):
        content = '@#hello'
        username_should_be = []
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)

    def test_search_username_with_sharp_between(self):
        content = '@h#ello'
        username_should_be = ['h']
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)

    def test_search_username_with_no_username(self):
        content = 'tweet content'
        username_should_be = []
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)

    def test_search_username_with_one_begin(self):
        content = '@hello tweet content'
        username_should_be = ['hello']
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)

    def test_search_username_with_one_not_begin(self):
        content = 'tweet @hello content'
        username_should_be = ['hello']
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)

    def test_search_username_with_one_no_space(self):
        content = 'tweet@hello content '
        username_should_be = ['hello']
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)

    def test_search_username_with_two_or_more_in_a_row(self):
        content = '@hello @world tweet content'
        username_should_be = ['hello', 'world']
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)

    def test_search_username_with_two_or_more_seperate(self):
        content = '@hello tweet @world content'
        username_should_be = ['hello', 'world']
        usernames = handler.search_username(content)
        self.assertEqual(usernames, username_should_be)


    def test_get_notification_subtitle_should_be_followed(self):
        notificate_type = 'F'
        subtitle_should_be = 'Followed you'
        subtitle = handler.get_notification_subtitle(notificate_type, tweet=None)
        self.assertEqual(subtitle, subtitle_should_be)

    def test_get_notification_subtitle_should_be_replied(self):
        notificate_type = 'T'
        tweet = self.reply_from_admin_to_admin
        subtitle_should_be = 'Replied your tweet'
        subtitle = handler.get_notification_subtitle(notificate_type, tweet)
        self.assertEqual(subtitle, subtitle_should_be)

    def test_get_notification_subtitle_should_be_replied_retweet(self):
        notificate_type = 'T'
        tweet = self.retweet_from_admin_to_admin
        subtitle_should_be = 'Replied your Retweet'
        subtitle = handler.get_notification_subtitle(notificate_type, tweet)
        self.assertEqual(subtitle, subtitle_should_be)

    
        

