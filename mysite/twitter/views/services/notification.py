from .share import *

def get_notification_subtitle(notificate_type):

    notification_type_subtitle = [
        (Notification.MENTION, 'Mentioned you.'),
        (Notification.REPLY, 'Replied your tweet'),
        (Notification.RETWEET, 'Retweeted your tweet'),
        (Notification.RETWEET_MENTION, 'Retweet the tweet mentioned you'),
        (Notification.LIKE, 'Liked your tweet'),
        (Notification.LIKE_MENTION, 'Liked the tweet mentioned you'),
        (Notification.FOLLOW, 'Followed you')
    ]
    for kind, subtitle in notification_type_subtitle:
        if kind == notificate_type:
            return subtitle