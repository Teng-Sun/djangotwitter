from django.conf.urls import url
from . import views
from twitter.views import pages, tweets, users

urlpatterns = [
    url(r'^$', pages.index, name='index'),

    url(r'^moment/today$', pages.today, name='today'),
    url(r'^moment/top$', pages.top, name='top'),


    
    url(r'^notification/$', pages.notification, name='notification'),
    url(r'^profile/(?P<username>\w+)/$', pages.profile, name='profile'),
    url(r'^tweet/$', pages.post_tweet, name='post_tweet'),
    url(r'^follower/(?P<username>\w+)/$', pages.follower, name="follower"),
    url(r'^following/(?P<username>\w+)/$', pages.following, name="following"),
    url(r'^likes/(?P<username>\w+)/$', pages.likes, name='likes'),
    
    
    url(r'^explore/$', pages.explore, name='explore'),

    url(r'^accounts/register/$', users.register, name='register'),
    url(r'^follow/(?P<username>\w+)/$', users.follow, name="follow"),
    url(r'^unfollow/(?P<username>\w+)/$', users.unfollow, name="unfollow"),
    

    url(r'^reply/(?P<tweet_id>\w+)/$', tweets.reply, name="reply"),
    url(r'^retweet/(?P<tweet_id>\w+)$', tweets.retweet, name="retweet"),
    url(r'^unretweet/(?P<tweet_id>\w+)$', tweets.unretweet, name="unretweet"),
    url(r'^like/(?P<tweet_id>\w+)$', tweets.like, name='like'),
    url(r'^unlike/(?P<tweet_id>\w+)$', tweets.unlike, name='unlike'),
    url(r'^delete/(?P<tweet_id>\w+)$', tweets.delete, name='delete'),
]