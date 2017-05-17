from django.contrib.auth.models import User
from django.test import TestCase

from twitter.models import Tweet
from twitter.views.services import post

class PostTest(TestCase):
    fixtures = [
        'twitter/fixtures/test_user_data.json',
        'twitter/fixtures/test_tweet_data.json',
        'twitter/fixtures/test_followship_data.json',
        'twitter/fixtures/test_replyship_data.json',
        'twitter/fixtures/test_like_data.json'
    ]

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')

        self.tweet_a = Tweet.objects.get(pk=1)
        self.retweet_a_re_1 = Tweet.objects.get(pk=12)
        self.tweet_1_m_all = Tweet.objects.get(pk=6)
        self.tweet_2 = Tweet.objects.get(pk=3)
        self.tweet_no_reply = Tweet.objects.get(pk=4)


        self.reply_a_r_2 = Tweet.objects.get(pk=13)
        self.a_reply_a_r_2 = Tweet.objects.get(pk=14)
        self.user1_reply_a_r_2 = Tweet.objects.get(pk=15)
        self.user2_reply_1_to_a_r_2 = Tweet.objects.get(pk=16)
        self.a_reply_2_to_1_to_a_r_2 = Tweet.objects.get(pk=17)
        self.user2_reply_a_r_2 = Tweet.objects.get(pk=18)

        self.a_re_a = Tweet.objects.get(pk=10)
        self.a_like_a = Tweet.objects.get(pk=5)

    def test_get_original(self):
        data = [
            (self.tweet_a, self.tweet_a),
            (self.retweet_a_re_1, self.tweet_1_m_all)
        ]
        for t, original in data:
            self.assertEqual(post.get_original(t), original)

    def test_get_reply_replies(self):
        data = [
            (self.reply_a_r_2, set([14, 15, 16, 17, 18])),
            (self.a_reply_a_r_2, set([18])),
            (self.user1_reply_a_r_2, set([16, 17])),
            (self.user2_reply_1_to_a_r_2, set([17])),
            (self.a_reply_2_to_1_to_a_r_2, set([])),
            (self.user2_reply_a_r_2, set([]))
        ]
        for reply, result in data:
            reply_list = []
            reply_ids = set([])
            post.get_reply_replies(reply, reply_list)
            for reply_item in reply_list:
                reply_ids.add(reply_item.id)
            self.assertEqual(reply_ids, result)

    def test_get_tweet_replies(self):
        data = [
            (self.tweet_no_reply, []),
            (self.tweet_2, [[13, 15, 16, 17, 14, 18]]),
            (self.tweet_a, [[8], [7,19]]),
        ]

        for t, result in data:
            replies_list = []
            replies_ids = []
            post.get_tweet_replies(t, replies_list)
            for index, reply_list in enumerate(replies_list):
                replies_ids.append([])
                for item in reply_list:
                    replies_ids[index].append(item.id)
            self.assertEqual(replies_ids, result)

    def test_been_retweeted(self):
        data = [
            (self.tweet_a, self.admin, True),
            (self.tweet_a, self.user1, False),
        ]
        for t, user, result in data:
            self.assertEqual(post.been_retweeted(t, user), result)
            
    def test_been_liked(self):
        data = [
            (self.a_like_a, self.admin, True),
            (self.a_like_a, self.user1, False),
        ]
        for t, user, result in data:
            self.assertEqual(post.been_liked(t, user), result)