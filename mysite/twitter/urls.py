from django.conf.urls import url
from . import views
from twitter.views import base
from twitter.views import tweet

urlpatterns = [
    url(r'^$', base.index, name='index'),
    url(r'^tweet/$', base.post_tweet, name='post_tweet'),
    url(r'^profile/(?P<username>\w+)/$', base.profile, name='profile'),
    url(r'^accounts/register/$', base.register, name='register'),
    url(r'^explore/$', base.explore, name='explore'),
    url(r'^follower/(?P<username>\w+)/$', base.follower, name="follower"),
    url(r'^following/(?P<username>\w+)/$', base.following, name="following"),
    url(r'^likes/(?P<username>\w+)/$', base.likes, name='likes'),
    url(r'^follow/(?P<username>\w+)/$', base.follow, name="follow"),
    url(r'^unfollow/(?P<username>\w+)/$', base.unfollow, name="unfollow"),

    url(r'^reply/(?P<tweet_id>\w+)/$', tweet.reply, name="reply"),
    url(r'^retweet/(?P<tweet_id>\w+)$', tweet.retweet, name="retweet"),
    url(r'^unretweet/(?P<tweet_id>\w+)$', tweet.unretweet, name="unretweet"),
    url(r'^like/(?P<tweet_id>\w+)$', tweet.like, name='like'),
    url(r'^unlike/(?P<tweet_id>\w+)$', tweet.unlike, name='unlike'),
]