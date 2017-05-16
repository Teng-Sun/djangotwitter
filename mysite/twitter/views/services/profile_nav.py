from .share import *
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

# def subnav_sessions(login_user, visited_user):
#     session_key = set_profile_subnav_sessions(login_user, visited_user)
#     sessions = SessionStore(session_key=session_key)
#     return sessions

def subnav_sessions(request, login_user, visited_user):
    login_follow_visited = check_followship(login_user, visited_user)
    tweet, following, follower, like = get_subnav_data(visited_user)
    subnav_data = [
        ('tweet_num', tweet),
        ('following_num', following),
        ('follower_num', follower),
        ('like_num', like),
        ('login_follow_visited', login_follow_visited),
    ]
    set_sessions(request, subnav_data)

def check_followship(initiative_user, followed_user):
    return bool(Followship.objects.filter(
        initiative_user=initiative_user,
        followed_user=followed_user
    ))

def set_sessions(request, data):
    for key, value in data:
        request.session[key] = value

def get_subnav_data(user):
    tweet_num = len(Tweet.objects.filter(author=user, original_tweet__isnull=True))
    following_num = len(Followship.objects.filter(initiative_user=user))
    follower_num = len(Followship.objects.filter(followed_user=user))
    like_num = len(Like.objects.filter(author=user))
    return tweet_num, following_num, follower_num, like_num