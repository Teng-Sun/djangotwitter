from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from twitter.models import Tweet, Like
from twitter.forms import ReplyForm

import handler
# from .handler import *
from .base import *
from .tweet import *


@login_required
def retweet(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user

    original_tweet = handler.get_original_tweet(tweet)

    if not Tweet.objects.filter(author=user, original_tweet=original_tweet):
        
        original_tweet.retweet_num += 1
        original_tweet.save()

        new_tweet = handler.create_tweet(user, original_tweet.content, original_tweet, date=None)
        new_tweet.save()
   
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unretweet(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user

    original_tweet = handler.get_original_tweet(tweet)

    if Tweet.objects.filter(author=user, original_tweet=original_tweet):
        original_tweet.retweet_num -= 1
        original_tweet.save()
        tweet.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def reply(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user
    original_tweet = handler.get_original_tweet(tweet)
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.tweet = original_tweet
            reply.author = user
            reply.save()

            new_tweet = handler.create_tweet(user, reply.content, original_tweet=None, date=None)
            new_tweet.save()
    else:
        reply_form = ReplyForm()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def like(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    original_tweet = handler.get_original_tweet(tweet)
    user = request.user
    if not Like.objects.filter(tweet=original_tweet, author=user):
        new_like = Like(
            author = user,
            tweet = tweet,
        )
        new_like.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unlike(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    original_tweet = handler.get_original_tweet(tweet)
    user = request.user
    like = Like.objects.get(tweet=original_tweet, author=user)
    if like:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER'))