from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from .models import Tweet, Followship
from .forms import TweetForm, RegistrationForm, FollowForm

def index(request):
    return render(request, 'twitter/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user = User.objects.create_user(
                request.POST.get('username'),
                request.POST.get('email'),
                request.POST.get('password'),
            )
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {
        'form': form,
    })

def add_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('profile', username=request.user.username)
    else:
        form = TweetForm()
    return render(request, 'twitter/add_tweet.html', {
        'form': form,
    })

def profile(request, username):
    visited_user, tweet_list, following_list, \
        follower_list = set_profile_subnav_session(request, username)

    paginate_by = 10
    tweets = pagination(request, tweet_list, paginate_by)

    return render(request, 'twitter/profile.html', {
        'visited_user': visited_user,
        'tweets': tweets,
        'object_list': tweets,
    })

def following(request, username):
    visited_user, tweet_list, following_list, \
        follower_list = set_profile_subnav_session(request, username)
    paginate_by = 10
    followings = pagination(request, following_list, paginate_by)
    return render(request, 'twitter/following.html', {
        'visited_user': visited_user,
        'followings': followings,
        'object_list': followings,
    })

def follower(request, username):
    visited_user, tweet_list, following_list, \
        follower_list = set_profile_subnav_session(request, username)
    paginate_by = 10
    followers = pagination(request, follower_list, paginate_by)
    return render(request, 'twitter/follower.html', {
        'visited_user': visited_user,
        'followers': followers,
        'object_list': followers,
    })


# TODO
def explore(request):
    user_list = User.objects.all()
    tweet_list = []
    tweets = []
    if user_list:
        for user in user_list:
            if user.tweet_set.all():
                tweet_list.append(user.tweet_set.all()[0])
    paginate_by = 10
    tweets = pagination(request, tweet_list, paginate_by)
    return render(request, 'twitter/explore.html', {
        'tweets': tweets,
    })


# def follow(request, username):
#     login_user = request.user
#     visited_user = User.objects.get(username=username)

#     if login_user != visited_user and request.method == 'POST':
#         login_follow_visited, _ = validate_followship(login_user, visited_user)

#         if not login_follow_visited:
#             form = FollowForm(request.POST)
#             form.save(commit=False)
#             follow = Followship(
#                 followed_user = visited_user,
#                 initiative_user = login_user,
#             )
#             follow.save()
#     return redirect('profile', username=username)


def profile_subnav(username):
    visited_user = User.objects.get(username=username)
    tweet_list = visited_user.tweet_set.all()
    following_list = Followship.objects.filter(initiative_user=visited_user).all()
    follower_list = Followship.objects.filter(followed_user=visited_user).all()
    return visited_user, tweet_list, following_list, follower_list

def validate_followship(login_user, visited_user):
    login_follow_visited = False
    visited_follow_login = False

    if Followship.objects.filter(followed_user=visited_user, initiative_user=login_user).all():
        login_follow_visited = True
    if Followship.objects.filter(followed_user=login_user, initiative_user=visited_user).all():
        visited_follow_login = True
    return login_follow_visited, visited_follow_login

def set_profile_subnav_session(request, username):
    login_user = request.user

    visited_user, tweet_list, following_list, \
        follower_list = profile_subnav(username)

    login_follow_visited, visited_follow_login, \
        = validate_followship(login_user, visited_user)

    request.session['tweet_num'] = len(tweet_list)
    request.session['following_num'] = len(following_list)
    request.session['follower_num'] = len(follower_list)

    request.session['login_follow_visited'] = login_follow_visited
    request.session['visited_follow_login'] = visited_follow_login

    return visited_user, tweet_list, following_list, follower_list


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
