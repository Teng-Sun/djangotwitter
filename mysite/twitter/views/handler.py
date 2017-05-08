from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

from twitter.models import Tweet, Replyship, Followship, Like, Notification, Stream
from twitter.forms import TweetForm, RegistrationForm

def check_followship(initiative_user, followed_user):
    return bool(Followship.objects.filter(
        initiative_user=initiative_user,
        followed_user=followed_user
    ))


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


def create_notification(initiative_user, notificated_user, notificate_type, tweet):
    notification = Notification(
        initiative_user = initiative_user,
        notificated_user = notificated_user,
        notificate_type = notificate_type,
    )
    if tweet:
        notification.tweet = tweet
    notification.save()

def search_username(content):
    reg = '@(\w+)'
    usernames = re.findall(reg, content)
    return usernames

def notificate_users(usernames, initiative_user, notificate_type, tweet):
    for username in usernames:
        user = User.objects.filter(username=username)
        if user:
            create_notification(initiative_user, user[0], notificate_type, tweet)

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


def create_tweet(author, content, original_tweet):
    new_tweet = Tweet(
        author = author,
        content = content,
    )
    if original_tweet:
        new_tweet.original_tweet = original_tweet

    new_tweet.save()


    usernames = search_username(content)
    if original_tweet:
        notificate_users(usernames, author, 'R', new_tweet)
    else:
        notificate_users(usernames, author, 'T', new_tweet)
    return new_tweet

    
def get_original_tweet(tweet):
    return tweet.original_tweet or tweet

def get_reply_replies(reply, reply_list):
    replyships = Replyship.objects.filter(tweet=reply)
    for replyship in replyships:
        new_reply = replyship.reply
        reply_list.append(new_reply)
        get_reply_replies(new_reply, reply_list)

def get_tweet_replies(tweet, replies_list):
    replyships = Replyship.objects.filter(tweet=tweet)
    for index, replyship in enumerate(replyships):
        reply = replyship.reply
        reply_list = [reply]
        get_reply_replies(reply, reply_list)
        replies_list.append([])
        replies_list[index] = reply_list

def get_tweet_data(tweet, visited_user, login_user):
    original_tweet = get_original_tweet(tweet)
    tweet.retweet_num = original_tweet.retweet_num
    tweet.like_num = original_tweet.like_num
    tweet.reply_num = original_tweet.reply_num
    if Like.objects.filter(author=login_user, tweet=original_tweet):
        tweet.has_been_liked = True
    if Tweet.objects.filter(author=login_user, original_tweet=original_tweet):
        tweet.has_been_retweeded = True
    tweet.replies_list = []
    get_tweet_replies(tweet, tweet.replies_list)
    return tweet
   
def get_show_tweets(tweet_list, visited_user, login_user):
    show_tweets = list(tweet_list)
    for tweet in tweet_list:
        get_tweet_data(tweet, visited_user, login_user)
        if Tweet.objects.filter(author=visited_user, original_tweet=tweet):
            show_tweets.remove(tweet)
    return show_tweets

def get_show_likes(likes, login_user):
    show_tweets = []
    for like in likes:
        tweet = like.tweet

        tweet.replies_list = []
        get_tweet_replies(tweet, tweet.replies_list)

        if Like.objects.filter(author=login_user, tweet=tweet):
            tweet.has_been_liked = True
        if Tweet.objects.filter(author=login_user, original_tweet=tweet):
            tweet.has_been_retweeded = True

        show_tweets.append(tweet)
    return show_tweets

def profile_subnav_title(request, username):
    visited_user = User.objects.get(username=username)
    tweet_num = len(Tweet.objects.filter(author=visited_user, original_tweet__isnull=True))
    following_num = len(Followship.objects.filter(initiative_user=visited_user))
    follower_num = len(Followship.objects.filter(followed_user=visited_user))
    like_num = len(Like.objects.filter(author=visited_user))

    return visited_user, tweet_num, following_num, follower_num, like_num

def set_profile_subnav_session(request, username):
    login_user = request.user
    visited_user, tweet_num, following_num, \
        follower_num, like_num = profile_subnav_title(request, username)

    request.session['tweet_num'] = tweet_num
    request.session['following_num'] = following_num
    request.session['follower_num'] = follower_num
    request.session['like_num'] = like_num
    request.session['login_follow_visited'] = bool(check_followship(login_user, visited_user))
    request.session['visited_follow_login'] = bool(check_followship(visited_user, login_user))
    return visited_user


def pagination(request, objcet_list, paginate_by):
    paginator = Paginator(objcet_list, paginate_by)
    page = request.GET.get('page', 1)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result