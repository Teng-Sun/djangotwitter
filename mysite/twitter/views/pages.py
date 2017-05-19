from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from twitter.models import Tweet, Followship, Like, Notification, Stream
from twitter.forms import TweetForm, RegistrationForm
from services import share, notify, stream, post, profile_nav

from services import page


def index(request):
    render_data = page.index(request)
    return render(request, 'twitter/index.html', render_data)

def notification(request):
    render_data = page.notification(request)
    return render(request, 'twitter/notification.html', render_data)

def profile(request, username):
    render_data = page.profile(request, username)
    return render(request, 'twitter/profile.html', render_data)

def following(request, username):
    render_data = page.following(request, username)
    return render(request, 'twitter/following.html', render_data)

def follower(request, username):
    render_data = page.follower(request, username)
    return render(request, 'twitter/follower.html', render_data)

def likes(request, username):
    render_data = page.likes(request, username)
    return render(request, 'twitter/likes.html', render_data)



@login_required
def post_tweet(request):
    login_user = request.user
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            new_tweet = post.create_tweet(login_user, tweet.content, None)
            notify.notify(login_user, new_tweet, Notification.MENTION)
            stream.create_streams(new_tweet, Stream.TWEET)
            return redirect('profile', username=login_user.username)
    else:
        form = TweetForm()
    return render(request, 'twitter/post_tweet.html', {
        'form': form,
    })

def explore(request):
    render_data = page.explore(request)
    return render(request, 'twitter/explore.html', render_data)