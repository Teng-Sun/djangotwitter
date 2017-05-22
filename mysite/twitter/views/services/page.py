from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from twitter.models import Tweet, Stream, Followship, Like, Notification
from . import post, share, notify, profile_nav

import datetime

def index(request):
    user = request.user
    stream_list = []
    if user.is_authenticated():
        streams = Stream.objects.filter(receiver=user)
        for s in streams:
            post.get_action_data(s.tweet, user)
        paginate_by = 10
        stream_list = share.pagination(request, streams, paginate_by)
    return {
        'stream_list': stream_list,
        'pagination_result': stream_list,
    }

def notification(request):
    user = request.user
    notifications = Notification.objects.filter(notified_user=user)
    for n in notifications:
        n.subtitle = notify.get_subtitle(n.notified_type)
        tweet = n.tweet
        if tweet:
            post.get_action_data(tweet, user)
    paginate_by = 10
    notification_list = share.pagination(request, notifications, paginate_by)
    return {
        'notification_list': notification_list,
        'pagination_result': notification_list,
    }

def profile(request, username):
    login_user = request.user
    visited_user = get_object_or_404(User, username=username)
    profile_nav.subnav_sessions(request, login_user, visited_user)
    tweet_list = list(Tweet.objects.filter(author=visited_user))

    tweets = post.show_tweets(tweet_list, visited_user, request.user)
    paginate_by = 10
    tweets = share.pagination(request, tweets, paginate_by)
    return {
        'visited_user': visited_user,
        'tweets': tweets,
        'pagination_result': tweets,
    }

def following(request, username):
    visited_user = get_object_or_404(User, username=username)
    following_list = Followship.objects.filter(initiative_user=visited_user)
    paginate_by = 10
    followings = share.pagination(request, following_list, paginate_by)
    return {
        'visited_user': visited_user,
        'followings': followings,
        'pagination_result': followings,
    }

def follower(request, username):
    visited_user = get_object_or_404(User, username=username)
    follower_list = Followship.objects.filter(followed_user=visited_user)
    paginate_by = 10
    followers = share.pagination(request, follower_list, paginate_by)
    return {
        'visited_user': visited_user,
        'followers': followers,
        'pagination_result': followers,
    }

def likes(request, username):
    login_user = request.user
    visited_user = get_object_or_404(User, username=username)
    likes = Like.objects.filter(author=visited_user)
    like_tweets = post.show_like_tweets(likes, login_user)
    paginate_by = 10
    like_tweets_list = share.pagination(request, like_tweets, paginate_by)
    return {
        'visited_user': visited_user,
        'tweets': like_tweets_list,
        'pagination_result': like_tweets_list,
    }

def post_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            new_tweet = post.create_tweet(request.user, tweet.content, None)
            notify.notify(request.user, new_tweet, Notification.MENTION)
            stream.create_streams(new_tweet, Stream.TWEET)
            return redirect('profile', username=request.user.username)
    else:
        form = TweetForm()
    return render(request, 'twitter/post_tweet.html', {
        'form': form,
    })

def explore(request):
    login_user = request.user
    users = User.objects.all()
    leasts = []
    likes = []
    retweets = []
    replies = []
    for user in users:
        tweets = Tweet.objects.filter(author=user, original_tweet__isnull=True)
        if tweets and tweets.first:
            leasts.append(tweets.first)
        post.select_tweet(tweets, 'like_num', login_user, likes)
        post.select_tweet(tweets, 'retweet_num', login_user, retweets)
        post.select_tweet(tweets, 'reply_num', login_user, replies)
    return {
        'leasts': leasts,
        'likes': likes,
        'retweets': retweets,
        'replies': replies
    }

def today(request):
    now = timezone.now()
    date = datetime.datetime(now.year, now.month, now.day)
    today = timezone.make_aware(date)
    tweets = Tweet.objects.filter(
        created_date__gte=today
    )
    todays = post.tweets_actions(tweets, request.user)
    paginate_by = 10
    items = share.pagination(request, todays, paginate_by)
    return {
        'items': items,
        'pagination_result': items,
    }

def top(request):
    tweets = Tweet.objects.filter(original_tweet__isnull=True
        ).order_by(
        '-retweet_num', '-created_date')
    tops = post.tweets_actions(tweets, request.user)
    paginate_by = 10
    items = share.pagination(request, tops, paginate_by)
    return {
        'items': items,
        'pagination_result': items,
    }

def engagement(request):
    tweets = Tweet.objects.order_by(
        '-reply_num', '-created_date')
    engagements = post.tweets_actions(tweets, request.user)
    paginate_by = 10
    items = share.pagination(request, engagements, paginate_by)
    return {
        'items': items,
        'pagination_result': items,
    }

def favorite(request):
    tweets = Tweet.objects.filter(original_tweet__isnull=True
        ).order_by('-like_num', '-created_date')
    favorites = post.tweets_actions(tweets, request.user)
    paginate_by = 10
    items = share.pagination(request, favorites, paginate_by)
    return {
        'items': items,
        'pagination_result': items,
    }