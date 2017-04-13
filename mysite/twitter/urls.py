from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tweet/$', views.add_tweet, name='add_tweet'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^explore/$', views.explore, name='explore'),
]