from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

from twitter.models import Tweet, Replyship, Followship, Like, Notification, Stream
from twitter.forms import TweetForm, RegistrationForm

def search_username(content):
    reg = '@(\w+)'
    usernames = re.findall(reg, content)
    return usernames

def create_notification(initiative_user, notificated_user, notificate_type, tweet):
    notification = Notification(
        initiative_user = initiative_user,
        notificated_user = notificated_user,
        notificate_type = notificate_type,
    )
    if tweet:
        notification.tweet = tweet
    notification.save()

def notificate_users(usernames, initiative_user, notificate_type, tweet):
    for username in usernames:
        user = User.objects.filter(username=username)
        if user:
            create_notification(initiative_user, user[0], notificate_type, tweet)

def check_followship(initiative_user, followed_user):
    return bool(Followship.objects.filter(
        initiative_user=initiative_user,
        followed_user=followed_user
    ))
    
def pagination(request, objcet_list, paginate_by):
    paginator = Paginator(objcet_list, paginate_by)
    page = request.GET.get('page', 1)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result