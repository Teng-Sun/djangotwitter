from .share import *


def get_notification_subtitle(notificate_type):
    notification_type_subtitle = [
        ('T', 'Replied your tweet'),
        ('L', 'Liked your tweet'),
        ('R', 'Retweeted your tweet'),
        ('F', 'Followed you')
    ]
    for kind, subtitle in notification_type_subtitle:
        if kind == notificate_type:
            return subtitle