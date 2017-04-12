from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Tweet
from .forms import TweetForm

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
    return render(request, 'twitter/profile.html', {
        'user': request.user
    })