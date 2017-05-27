from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from twitter.models import Tweet, Replyship, Like

@receiver(post_save, sender=Tweet)
def post_save_retweet(sender, **kwargs):
    retweet = kwargs.get('instance')
    operate_num(retweet, 'retweet_num', is_increase=True)
    
@receiver(post_delete, sender=Tweet)
def post_delete_retweet(sender, **kwargs):
    retweet = kwargs.get('instance')
    operate_num(retweet, 'retweet_num', is_increase=False)

@receiver(post_save, sender=Replyship)
def post_save_replyship(sender, **kwargs):
    replyship = kwargs.get('instance')
    operate_num(replyship, 'reply_num', is_increase=True)

@receiver(post_delete, sender=Replyship)
def post_delete_replyship(sender, **kwargs):
    replyship = kwargs.get('instance')
    operate_num(replyship, 'reply_num', is_increase=False)

@receiver(post_save, sender=Like)
def post_save_like(sender, **kwargs):
    like = kwargs.get('instance')
    operate_num(like, 'like_num', is_increase=True)

@receiver(post_delete, sender=Like)
def post_delete_like(sender, **kwargs):
    like = kwargs.get('instance')
    operate_num(like, 'like_num', is_increase=False)

def get_tweet(instance):
    if hasattr(instance, 'original_tweet'):
        tweet = instance.original_tweet
    elif hasattr(instance, 'tweet'):
        tweet = instance.tweet
    else:
        tweet = None
    return tweet

def operate_num(instance, num, is_increase):
    tweet = get_tweet(instance)
    if tweet:
        if is_increase:
            number = getattr(tweet, num) + 1
        else:
            number = getattr(tweet, num) - 1
        setattr(tweet, num, number)
        tweet.save()