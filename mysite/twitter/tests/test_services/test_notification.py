from django.test import TestCase

from twitter.views.services import notification
from twitter.models import Notification

class NotificationTest(TestCase):
   
    def test_get_notification_subtitle(self):
        data = [
            (Notification.REPLY, 'Replied your tweet'),
            (Notification.MENTION, 'Mentioned you in the tweet'),
            (Notification.RETWEET, 'Retweeted your tweet'),
            (Notification.RETWEET_MENTION, 'Retweet the tweet mentioned you'),
            (Notification.LIKE, 'Liked your tweet'),
            (Notification.FOLLOW, 'Followed you')
        ]

        for notificate_type, result in data:
            subtitle = notification.get_notification_subtitle(notificate_type)
            self.assertEquals(subtitle, result)
