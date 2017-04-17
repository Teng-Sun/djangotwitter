from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tweet/$', views.add_tweet, name='add_tweet'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^explore/$', views.explore, name='explore'),
    url(r'^follower/(?P<username>\w+)/$', views.follower, name="follower"),
    url(r'^following/(?P<username>\w+)/$', views.following, name="following"),
    url(r'^follow/(?P<username>\w+)/$', views.follow, name="follow"),
    url(r'^unfollow/(?P<username>\w+)/$', views.unfollow, name="unfollow"),
]