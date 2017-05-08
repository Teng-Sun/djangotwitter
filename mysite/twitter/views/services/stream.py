from .share import *

def cretae_stream(receiver, tweet, stream_type):
    stream = Stream(
        receiver = receiver,
        tweet = tweet,
        stream_type = stream_type,
    )
    stream.save()

def get_receivers(tweet, stream_type):
    user = tweet.author
    receivers = set([user])
    followships = Followship.objects.filter(followed_user=user)
    for followship in followships:
        follower = followship.initiative_user
        if stream_type == 'Y':
            replyships = Replyship.objects.filter(reply=tweet)
            if replyships:
                reply_user = replyships[0].reply_user
                be_replied_user = replyships[0].tweet_user

                be_replied_user_followship = check_followship(be_replied_user, user)
                follower_followship = check_followship(follower, be_replied_user)

                if be_replied_user_followship:
                    receivers.add(be_replied_user)
                if follower_followship:
                    receivers.add(follower)
        else:
            receivers.add(follower)
    return receivers

def create_streams(tweet, stream_type):
    receivers = get_receivers(tweet, stream_type)
    for receiver in receivers:
        cretae_stream(receiver, tweet, stream_type)