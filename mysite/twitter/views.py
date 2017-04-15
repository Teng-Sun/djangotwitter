from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Tweet, Followship
from .forms import TweetForm, RegistrationForm, FollowForm

def index(request):
    return render(request, 'twitter/index.html')

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
    login_user = request.user
    visited_user = User.objects.get(username=username)
    tweet_list = visited_user.tweet_set.all()
    paginate_by = 10
    tweets = pagination(request, tweet_list, paginate_by)
    following = Followship.objects.filter(initiative_user=visited_user).all()
    follower = Followship.objects.filter(followed_user=visited_user).all()
    return render(request, 'twitter/profile.html', {
        'visited_user': visited_user,
        'tweets': tweets,
        'object_list': tweets,
        'following': following,
        'follower': follower,
    })

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


def follow(request, username):
    login_user = request.user
    visited_user = User.objects.get(username=username)
    if login_user != visited_user and request.method == 'POST':
        form = FollowForm(request.POST)
        form.save(commit=False)
        follow = Followship(
            followed_user = visited_user,
            initiative_user = login_user,
        )
        follow.save()
    return redirect('profile', username=username)

def following(request, username):
    visited_user = User.objects.get(username=username)
    following_list = Followship.objects.filter(initiative_user=visited_user).all()
    paginate_by = 10
    followings = pagination(request, following_list, paginate_by)
    return render(request, 'twitter/following.html', {
        'followings': followings,
        'object_list': followings,
    })


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
