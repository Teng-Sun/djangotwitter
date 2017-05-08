from django.conf.urls import url
from . import views
from twitter.views import pages
from twitter.views import tweets

urlpatterns = [
    url(r'^$', pages.index, name='index'),
    url(r'^tweet/$', pages.post_tweet, name='post_tweet'),
    url(r'^profile/(?P<username>\w+)/$', pages.profile, name='profile'),
    url(r'^accounts/register/$', pages.register, name='register'),
    url(r'^explore/$', pages.explore, name='explore'),
    url(r'^follower/(?P<username>\w+)/$', pages.follower, name="follower"),
    url(r'^following/(?P<username>\w+)/$', pages.following, name="following"),
    url(r'^likes/(?P<username>\w+)/$', pages.likes, name='likes'),
    url(r'^follow/(?P<username>\w+)/$', pages.follow, name="follow"),
    url(r'^unfollow/(?P<username>\w+)/$', pages.unfollow, name="unfollow"),
    url(r'^notification/$', pages.notification, name='notification'),

    url(r'^reply/(?P<tweet_id>\w+)/$', tweets.reply, name="reply"),
    url(r'^retweet/(?P<tweet_id>\w+)$', tweets.retweet, name="retweet"),
    url(r'^unretweet/(?P<tweet_id>\w+)$', tweets.unretweet, name="unretweet"),
    url(r'^like/(?P<tweet_id>\w+)$', tweets.like, name='like'),
    url(r'^unlike/(?P<tweet_id>\w+)$', tweets.unlike, name='unlike'),
    url(r'^delete/(?P<tweet_id>\w+)$', tweets.delete, name='delete'),
]