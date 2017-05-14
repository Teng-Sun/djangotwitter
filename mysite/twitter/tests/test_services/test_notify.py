from django.test import TestCase
from django.contrib.auth.models import User

from copy import copy

from twitter.views.services import notify
from twitter.models import Notification, Tweet

class NotifyTest(TestCase):

    fixtures = [
        'twitter/fixtures/test_user_data.json',
        'twitter/fixtures/test_tweet_data.json',
        'twitter/fixtures/test_like_data.json',
    ]

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')

        self.tweet_a = Tweet.objects.get(pk=1)
        self.tweet_1 = Tweet.objects.get(pk=2)
        self.tweet_a_m_not = Tweet.objects.get(pk=4)
        self.tweet_a_m_all = Tweet.objects.get(pk=5)


        self.reply_a_r_a = Tweet.objects.get(pk=7)
        self.reply_a_r_a_m_a = Tweet.objects.get(pk=8)
        self.reply_a_r_1_m_all = Tweet.objects.get(pk=9)

        self.retweet_a = Tweet.objects.get(pk=10)
        self.retweet_a_re_a_m_all = Tweet.objects.get(pk=10)
        self.retweet_a_re_1_m_all = Tweet.objects.get(pk=11)


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
            username = notify.search_username(content)
            self.assertEqual(username, username_should_be)

    def test_mention_receivers(self):
        data = [
            (self.admin, self.admin, self.tweet_a, set()),
            (self.admin, self.admin, self.tweet_a_m_not, set()),
            (self.admin, self.admin, self.tweet_a_m_all, set([self.user1, self.user2])),
            (self.admin, self.user1, self.reply_a_r_1_m_all, set([self.user2])),
        ]
        for notify_user, notified_user, tweet, results in data:
            receivers = notify.mention_receivers(notify_user, notified_user, tweet)
            self.assertEqual(receivers, results)

    def test_mention_type(self):
        data = [
            (Notification.MENTION, Notification.MENTION),
            (Notification.LIKE, Notification.LIKE_MENTION),
            (Notification.RETWEET, Notification.RETWEET_MENTION),
        ]
        for notified_type, result in data:
            n_type = notify.mention_type(notified_type)
            self.assertEqual(n_type, result)

    def test_notify_mention(self):
        data = [
            (self.admin, self.admin, self.tweet_a, Notification.MENTION),
            (self.admin, self.admin, self.tweet_a_m_not, Notification.MENTION),
            (self.admin, self.admin, self.tweet_a_m_all, Notification.MENTION),
            (self.admin, self.user1, self.reply_a_r_1_m_all, Notification.REPLY),
            (self.admin, self.user1, self.retweet_a_re_1_m_all, Notification.RETWEET),
            (self.admin, self.admin, self.tweet_a_m_all, Notification.LIKE)
        ]
        for notify_user, notified_user, tweet, n_type in data:
            Notification.objects.all().delete()
            notified_users = set()
            notify.notify_mention(notify_user, notified_user, tweet, n_type)

            notifications = Notification.objects.all()
            receivers = notify.mention_receivers(notify_user, notified_user, tweet)
            result_type = notify.mention_type(n_type)

            for item in notifications:
                self.assertEqual(item.notify_user, notify_user)
                self.assertEqual(item.tweet, tweet)
                self.assertEqual(item.notified_type, result_type)
                notified_users.add(item.notified_user)
            self.assertEqual(notified_users, receivers)

    def test_notify_follow(self):
        data = [
            [self.admin, self.user1],
            [self.admin, self.user2],
        ]
        for notify_user, notified_user in data:
            Notification.objects.all().delete()
            notify.notify_follow(notify_user, notified_user)
            notifications = Notification.objects.all()
            for item in notifications:
                self.assertEqual(item.notify_user, notify_user)
                self.assertEqual(item.notified_user, notified_user)
                self.assertEqual(item.notified_type, Notification.FOLLOW)
                self.assertFalse(item.tweet)

    def test_notify_reply(self):
        data = [
            [self.reply_a_r_a, self.tweet_a],
            [self.reply_a_r_a_m_a, self.tweet_a],
            [self.reply_a_r_1_m_all, self.tweet_1]
        ]
        for reply, tweet in data:
            Notification.objects.all().delete()
            notified_users = set()
            notify_user = reply.author

            notify.notify_reply(reply, tweet)
            notifications = Notification.objects.filter(tweet=reply)

            mention_receivers = notify.mention_receivers(notify_user, tweet.author, reply)
            receivers = copy(mention_receivers)
            
            if notify_user != tweet.author:
                receivers.add(tweet.author)
            for item in notifications:
                notified_users.add(item.notified_user)
                self.assertEqual(item.notify_user, notify_user)
                self.assertEqual(item.tweet, reply)
                if item.notified_user in mention_receivers:
                    self.assertEqual(item.notified_type, Notification.MENTION)
                else:
                    self.assertEqual(item.notified_type, Notification.REPLY)
            self.assertEqual(notified_users, receivers)

    def test_notify(self):
        data = [
            #tweet
            (self.admin, self.tweet_a, Notification.MENTION),
            (self.admin, self.tweet_a_m_not, Notification.MENTION),
            (self.admin, self.tweet_a_m_all, Notification.MENTION),
            #retweet
            (self.admin, self.tweet_a_m_all, Notification.RETWEET),
            #like
            (self.admin, self.tweet_a_m_all, Notification.LIKE)
        ]

        for notify_user, tweet, notified_type in data:
            Notification.objects.all().delete()
            notified_users = set()
            notify.notify(notify_user, tweet, notified_type)
            items = Notification.objects.all()

            mention_receivers = notify.mention_receivers(notify_user, tweet.author, tweet)
            receivers = copy(mention_receivers)
            if notify_user != tweet.author:
                receivers.add(tweet.author)
            for item in items:
                self.assertEqual(item.notify_user, notify_user)
                self.assertEqual(item.tweet, tweet)

                if item.notified_user in mention_receivers:
                    notified_type = notify.mention_type(notified_type)
                self.assertEqual(item.notified_type, notified_type)

                notified_users.add(item.notified_user)

            self.assertEqual(notified_users, receivers)

    def test_get_subtitle(self):
        data = [
            (Notification.MENTION, 'Mentioned you.'),
            (Notification.REPLY, 'Replied your tweet'),
            (Notification.RETWEET, 'Retweeted your tweet'),
            (Notification.RETWEET_MENTION, 'Retweeted the tweet mentioned you'),
            (Notification.LIKE, 'Liked your tweet'),
            (Notification.LIKE_MENTION, 'Liked the tweet mentioned you'),
            (Notification.FOLLOW, 'Followed you')
        ]
        for notified_type, subtitle in data:
            result = notify.get_subtitle(notified_type)
            self.assertEqual(subtitle, result)