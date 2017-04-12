from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Tweet
from .forms import TweetForm, RegistrationForm

def tweet_list(request):
    return render(request, 'twitter/tweet_list.html', {})

def add_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('/profile/')
    else:
        form = TweetForm()
    return render(request, 'twitter/add_tweet.html', {
        'form': form,
    })

def profile(request):
    tweet_list = request.user.tweet_set.all()
    paginate_by = 5
    tweets = pagination(request, tweet_list, paginate_by)
    return render(request, 'twitter/profile.html', {
        'user': request.user,
        'tweets': tweets,
        'object_list': tweets,
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
