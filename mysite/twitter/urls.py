from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tweet/$', views.add_tweet, name='add_tweet'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^explore/$', views.explore, name='explore'),
    url(r'^follow/(?P<username>\w+)/$', views.follow, name="follow"),
]