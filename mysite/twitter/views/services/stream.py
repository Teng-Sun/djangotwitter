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
    receivers = [author]
    followships = Followship.objects.filter(followed_user=user)
    for followship in followships:
        follower = followship.initiative_user
        if is_receiver(tweet, follower):
            receivers.append(follower)



# def get_receivers(tweet, stream_type):
#     user = tweet.author
#     receivers = set([user])
#     followships = Followship.objects.filter(followed_user=user)
#     for followship in followships:
#         follower = followship.initiative_user
#         if stream_type == 'Y':
#             replyships = Replyship.objects.filter(reply=tweet)
#             if replyships:
#                 reply_user = replyships[0].reply_user
#                 be_replied_user = replyships[0].tweet_user

#                 if be_replied_user == follower or check_followship(follower, be_replied_user):
#                     receivers.add(follower)
#         else:
#             receivers.add(follower)
#     return receivers

def create_streams(tweet, stream_type):
    receivers = get_receivers(tweet, stream_type)
    for receiver in receivers:
        cretae_stream(receiver, tweet, stream_type)