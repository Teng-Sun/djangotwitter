from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.tweet_list, name='tweet_list'),
    url(r'^tweet/$', views.add_tweet, name='add_tweet'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^accounts/register/$', views.register, name='register'),
]