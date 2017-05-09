from .share import *

def cretae_stream(receiver, tweet, stream_type):
    stream = Stream(
        receiver = receiver,
        tweet = tweet,
        stream_type = stream_type,
    )
    stream.save()

def is_receiver(tweet, follower):
    author = tweet.author
    replyship = Replyship.objects.filter(reply=tweet)
    if not replyship:
        return True
    else:
        replied_user = replyship[0].tweet_user
        follower_follows_replied_user = check_followship(follower, replied_user)
        return replied_user==follower or follower_follows_replied_user

def get_receivers(tweet):
    author = tweet.author
    receivers = set([author])
    followships = Followship.objects.filter(followed_user=author)
    for followship in followships:
        follower = followship.initiative_user
        if is_receiver(tweet, follower):
            receivers.add(follower)
    return receivers

def create_streams(tweet, stream_type):
    receivers = get_receivers(tweet)
    for receiver in receivers:
        cretae_stream(receiver, tweet, stream_type)