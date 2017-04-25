from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tweet/$', views.post_tweet, name='post_tweet'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^explore/$', views.explore, name='explore'),
    url(r'^follower/(?P<username>\w+)/$', views.follower, name="follower"),
    url(r'^following/(?P<username>\w+)/$', views.following, name="following"),
    url(r'^follow/(?P<username>\w+)/$', views.follow, name="follow"),
    url(r'^unfollow/(?P<username>\w+)/$', views.unfollow, name="unfollow"),
    url(r'^reply/(?P<tweet_id>\w+)/$', views.reply, name="reply"),
    url(r'^retweet/(?P<tweet_id>\w+)$', views.retweet, name="retweet"),
    url(r'^unretweet/(?P<tweet_id>\w+)/(?P<original_tweet_id>\w+)$', views.unretweet, name="unretweet"),
]