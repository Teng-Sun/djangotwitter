from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

from twitter.models import Tweet, Replyship, Followship, Like, Notification, Stream
from twitter.forms import TweetForm, RegistrationForm


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