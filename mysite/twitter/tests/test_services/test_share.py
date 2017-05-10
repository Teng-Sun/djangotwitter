from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from twitter.views.services import share
from twitter.models import Notification, Tweet


class ShareTest(TestCase):
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

    def test_notificate_users(self):
        data = [
            ([], None, None),
            (['user1', 'user2'], Notification.FOLLOW, None),
            (['user1'], Notification.REPLY, self.reply_from_admin_to_user1),
            (['admin'], Notification.RETWEET, self.retweet_from_admin_to_admin)
        ]
        for usernames, notificate_type, tweet in data:
            share.notificate_users(usernames, self.admin, notificate_type, tweet)
            notifications = Notification.objects.filter(initiative_user=self.admin, tweet=tweet)
            if not usernames:
                self.assertFalse(notifications)
            else:
                for notification in notifications:
                    self.assertIn(notification.notificated_user.username, usernames)
                    self.assertEquals(notification.notificate_type, notificate_type)
                    self.assertEquals(notification.tweet, tweet)
                    self.assertEquals(notification.initiative_user, self.admin)

    def test_check_followship(self):
        admin_follows_user1 = share.check_followship(self.admin, self.user1)
        user1_follows_admin = share.check_followship(self.user1, self.admin)
        self.assertTrue(user1_follows_admin)
        self.assertFalse(admin_follows_user1)

        







