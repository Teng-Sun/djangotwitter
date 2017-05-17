from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from twitter.models import Tweet, Stream, Followship
from . import post, share, profile_nav


def index(request):
    user = request.user
    stream_list = []
    show_pagination = False
    if user.is_authenticated():
        streams = Stream.objects.filter(receiver=user)
        for s in streams:
            post.get_action_data(s.tweet, user)
        paginate_by = 10
        stream_list, show_pagination = share.pagination(request, streams, paginate_by)
    return {
        'stream_list': stream_list,
        'object_list': stream_list,
        'show_pagination': show_pagination,
    }

def notificaiton(request):
    user = request.user
    show_pagination = False
    notifications = Notification.objects.filter(notified_user=user)
    for n in notifications:
        n.subtitle = notify.get_subtitle(n.notified_type)
        tweet = n.tweet
        if tweet:
            post.get_action_data(tweet, user)
    paginate_by = 10
    notification_list, show_pagination = share.pagination(request, notifications, paginate_by)
    return {
        'notification_list': notification_list,
        'object_list': notification_list,
        'show_pagination': show_pagination,
    }

def profile(request, username):
    login_user = request.user
    visited_user = get_object_or_404(User, username=username)
    profile_nav.subnav_sessions(request, login_user, visited_user)
    tweet_list = list(Tweet.objects.filter(author=visited_user))

    tweets = post.show_tweets(tweet_list, visited_user, request.user)
    paginate_by = 10
    tweets, show_pagination = share.pagination(request, tweets, paginate_by)
    return {
        'visited_user': visited_user,
        'tweets': tweets,
        'object_list': tweets,
        'show_pagination': show_pagination,
    }

