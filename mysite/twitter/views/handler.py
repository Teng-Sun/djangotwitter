from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .handler import *
from .base import *
from .tweet import *


from twitter.models import Tweet, Reply, Followship

def get_original_tweet(tweet):
    original_tweet = tweet
    if tweet.original_tweet:
        original_tweet = Tweet.objects.get(pk=tweet.original_tweet.id)
    return original_tweet

def create_tweet(author, content, original_tweet, date):
    new_tweet = Tweet(
        author = author,
        content = content,
    )
    if original_tweet:
        new_tweet.original_tweet = original_tweet
    if date:
        new_tweet.created_date = date
    return new_tweet


def profile_subnav(request, username):
    visited_user = User.objects.get(username=username)
    login_user = request.user
    tweet_list = list(visited_user.tweet_set.all())

    for tweet in tweet_list:
        original_tweet = get_original_tweet(tweet)
        if Tweet.objects.filter(author=login_user, original_tweet=original_tweet):
            tweet.has_been_retweeded = True
        if Tweet.objects.filter(author=visited_user, original_tweet=tweet):
            tweet_list.remove(tweet)
        if tweet.original_tweet:
            tweet.retweet_num = tweet.original_tweet.retweet_num
        tweet.replies = Reply.objects.filter(tweet=original_tweet)

    following_list = Followship.objects.filter(initiative_user=visited_user).all()
    follower_list = Followship.objects.filter(followed_user=visited_user).all()
    return visited_user, tweet_list, following_list, follower_list

def validate_followship(login_user, visited_user):
    login_follow_visited = False
    visited_follow_login = False

    if Followship.objects.filter(followed_user=visited_user, initiative_user=login_user).all():
        login_follow_visited = True
    if Followship.objects.filter(followed_user=login_user, initiative_user=visited_user).all():
        visited_follow_login = True
    return login_follow_visited, visited_follow_login

def set_profile_subnav_session(request, username):
    login_user = request.user

    visited_user, tweet_list, following_list, \
        follower_list = profile_subnav(request, username)

    login_follow_visited, visited_follow_login, \
        = validate_followship(login_user, visited_user)

    request.session['tweet_num'] = len(tweet_list)
    request.session['following_num'] = len(following_list)
    request.session['follower_num'] = len(follower_list)

    request.session['login_follow_visited'] = login_follow_visited
    request.session['visited_follow_login'] = visited_follow_login

    return visited_user, tweet_list, following_list, follower_list

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