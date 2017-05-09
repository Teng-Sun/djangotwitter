from django.test import TestCase

from twitter.views.services import notification

class NotificationTest(TestCase):
   
    def test_get_notification_subtitle(self):
        data = [
            ('T', 'Replied your tweet'),
            ('L', 'Liked your tweet'),
            ('R', 'Retweeted your tweet'),
            ('F', 'Followed you')
        ]

        for notificate_type, result in data:
            subtitle = notification.get_notification_subtitle(notificate_type)
            self.assertEquals(subtitle, result)
