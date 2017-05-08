from .share import *


def get_notification_subtitle(notificate_type, tweet):
    if tweet:
        if tweet.original_tweet:
            if notificate_type == 'T':
                subtitle = 'Replied your Retweet'
            elif notificate_type == 'L':
                subtitle = 'Liked your Retweet'
            else:
                subtitle = 'Retweeted your Retweet'
        else:
            if notificate_type == 'T':
                subtitle = 'Replied your tweet'
            elif notificate_type == 'L':
                subtitle = 'Liked your tweet'
            else:
                subtitle = 'Retweeted your tweet'
    else:
        if notificate_type == 'F':
            subtitle = 'Followed you'
    return subtitle