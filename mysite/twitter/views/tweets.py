from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from twitter.models import Tweet, Replyship, Like, Notification, Stream
from twitter.forms import TweetForm
from services import notify, stream, post

from twitter.signals import tweet

@login_required
def retweet(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user

    original_tweet = post.get_original(tweet)

    if not Tweet.objects.filter(author=user, original_tweet=original_tweet):

        new_tweet = post.create_tweet(user, original_tweet.content, original_tweet)

        notify.notify(user, original_tweet, Notification.RETWEET)

        stream.create_streams(new_tweet, Stream.RETWEET)

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unretweet(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user

    original_tweet = post.get_original(tweet)
    if post.been_retweeted(original_tweet, user):
        tweet.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def reply(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user
    original_tweet = post.get_original(tweet)
    if request.method == 'POST':
        reply_form = TweetForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)

            reply = post.create_tweet(user, new_reply.content, original_tweet=None)
            replyship = Replyship(
                tweet = original_tweet,
                reply = reply,
                tweet_user = original_tweet.author,
                reply_user = user,
            )
            replyship.save()

            notify.notify_reply(reply, original_tweet)

            stream.create_streams(reply, Stream.REPLY)
    else:
        reply_form = TweetForm()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def like(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    original_tweet = post.get_original(tweet)
    user = request.user
    if not Like.objects.filter(tweet=original_tweet, author=user):
        new_like = Like(
            author = user,
            tweet = original_tweet,
        )
        new_like.save()
        notify.notify(user, original_tweet, Notification.LIKE)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unlike(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    original_tweet = post.get_original(tweet)
    user = request.user
    like = Like.objects.get(tweet=original_tweet, author=user)
    if like:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    if tweet and tweet.author == request.user:
        original_tweet = post.get_original(tweet)
        replyship = Replyship.objects.filter(reply=original_tweet)
        original_tweet.delete()
    
    return redirect(request.META.get('HTTP_REFERER'))