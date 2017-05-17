from django.contrib.auth.models import User
import re

from twitter.models import Notification

# save to db
def create_notification(tweet, notify_user, notified_user, notified_type):
    notification = Notification(
        notify_user = notify_user,
        notified_user = notified_user,
        notified_type = notified_type,
    )
    if tweet:
        notification.tweet = tweet
    notification.save()

# create notification when follow
def notify_follow(notify_user, notified_user):
    create_notification(None, notify_user, notified_user, Notification.FOLLOW)

# create notifications when reply
def notify_reply(reply, be_replied_tweet):
    notify_user = reply.author
    notified_user = be_replied_tweet.author
    if notify_user != notified_user:
        create_notification(reply, notify_user, notified_user, Notification.REPLY)
    notify_mention(notify_user, notified_user, reply, Notification.MENTION)

# notify post, like and retweet
def notify(notify_user, tweet, notified_type):
    notified_user = tweet.author
    if notify_user != notified_user:
        create_notification(tweet, notify_user, notified_user, notified_type)
    notify_mention(notify_user, notified_user, tweet, notified_type)


def get_subtitle(notified_type):
    subtitles = [
        (Notification.MENTION, 'Mentioned you.'),
        (Notification.REPLY, 'Replied your tweet'),
        (Notification.RETWEET, 'Retweeted your tweet'),
        (Notification.RETWEET_MENTION, 'Retweeted the tweet mentioned you'),
        (Notification.LIKE, 'Liked your tweet'),
        (Notification.LIKE_MENTION, 'Liked the tweet mentioned you'),
        (Notification.FOLLOW, 'Followed you')
    ]
    for kind, subtitle in subtitles:
        if kind == notified_type:
            return subtitle

# get mentioned users through tweet content
def search_username(content):
    reg = '@(\w+)'
    usernames = re.findall(reg, content)
    return usernames

# get mentioned receivers except notify_user and notified_user
def mention_receivers(notify_user, notified_user, tweet):
    receivers = set()
    usernames = search_username(tweet.content)
    for username in usernames:
        user = User.objects.filter(username=username).first()
        if user:
            receivers.add(user)
    receivers.discard(notified_user)
    receivers.discard(notify_user)
    return receivers

# get mention type
def mention_type(notified_type):
    if notified_type == Notification.RETWEET:
        return Notification.RETWEET_MENTION
    elif notified_type == Notification.LIKE:
        return Notification.LIKE_MENTION
    else:
        return notified_type

# notify users mentioned in the tweet content
def notify_mention(notify_user, notified_user, tweet, notified_type):
    notified_users = mention_receivers(notify_user, notified_user, tweet)
    n_type = mention_type(notified_type)
    for notified_user in notified_users:
        create_notification(tweet, notify_user, notified_user, n_type)