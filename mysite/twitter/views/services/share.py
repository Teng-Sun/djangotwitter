from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

from twitter.models import Tweet, Replyship, Followship, Like, Notification, Stream
from twitter.forms import TweetForm, RegistrationForm


def pagination(request, object_list, paginate_by):
    paginator = Paginator(object_list, paginate_by)
    page = request.GET.get('page', 1)
    try:
        text = paginator.page(page)
    except PageNotAnInteger:
        text = paginator.page(1)
    except EmptyPage:
        text = paginator.page(paginator.num_pages)
    if paginator.num_pages == 1:
        show_pagination = False
    else:
        show_pagination = True
    return text, show_pagination