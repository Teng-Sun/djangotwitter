from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .models import Tweet, Followship, Reply, Like
from .forms import TweetForm, RegistrationForm, ReplyForm



@login_required
def retweet(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user

    original_tweet = get_original_tweet(tweet)

    if not Tweet.objects.filter(author=user, original_tweet=original_tweet):
        
        original_tweet.retweet_num += 1
        original_tweet.save()

        new_tweet = create_tweet(user, original_tweet.content, original_tweet, date=None)
        new_tweet.save()
   
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unretweet(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user

    original_tweet = get_original_tweet(tweet)

    if Tweet.objects.filter(author=user, original_tweet=original_tweet):
        original_tweet.retweet_num -= 1
        original_tweet.save()
        tweet.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def reply(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user
    original_tweet = get_original_tweet(tweet)
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.tweet = original_tweet
            reply.author = user
            reply.save()

            new_tweet = create_tweet(user, reply.content, original_tweet=None, date=None)
            new_tweet.save()
    else:
        reply_form = ReplyForm()
    return redirect(request.META.get('HTTP_REFERER'))



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

@login_required
def post_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('profile', username=request.user.username)
    else:
        form = TweetForm()
    return render(request, 'twitter/post_tweet.html', {
        'form': form,
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



@login_required
def follow(request, username):
    login_user = request.user
    visited_user = User.objects.get(username=username)

    if login_user != visited_user:
        login_follow_visited, _ = validate_followship(login_user, visited_user)

        if not login_follow_visited:
            follow = Followship(
                followed_user = visited_user,
                initiative_user = login_user,
            )
            follow.save()
    return redirect('profile', username=username)

@login_required
def unfollow(request, username):
    login_user = request.user
    visited_user = User.objects.get(username=username)

    if login_user != visited_user:
        login_follow_visited, _ \
            = validate_followship(login_user, visited_user)
        if login_follow_visited:
            followship = Followship.objects.get(
                followed_user=visited_user, initiative_user=login_user
            )
            followship.delete()
    return redirect('profile', username=username)




@login_required
def like(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user
    if not Like.objects.filter(tweet=tweet, author=user):
        like_tweet = Like(
            author = user,
            tweet = tweet,
        )
        like_tweet.save()
    return redirect(request.META.get('HTTP_REFERER'))


def create_tweet(author, content, original_tweet, date):
    new_tweet = Tweet(
        author = author,
        content = content,
    )
    if original_tweet:
        new_tweet.original_tweet = original_tweet
    if date:
        new_tweet.created_date = date
    return new_tweet


def profile_subnav(request, username):
    visited_user = User.objects.get(username=username)
    login_user = request.user
    tweet_list = list(visited_user.tweet_set.all())

    for tweet in tweet_list:
        original_tweet = get_original_tweet(tweet)
        if Tweet.objects.filter(author=login_user, original_tweet=original_tweet):
            tweet.has_been_retweeded = True
        if Tweet.objects.filter(author=visited_user, original_tweet=tweet):
            tweet_list.remove(tweet)
        if tweet.original_tweet:
            tweet.retweet_num = tweet.original_tweet.retweet_num
        tweet.replies = Reply.objects.filter(tweet=original_tweet)

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
        follower_list = profile_subnav(request, username)

    login_follow_visited, visited_follow_login, \
        = validate_followship(login_user, visited_user)

    request.session['tweet_num'] = len(tweet_list)
    request.session['following_num'] = len(following_list)
    request.session['follower_num'] = len(follower_list)

    request.session['login_follow_visited'] = login_follow_visited
    request.session['visited_follow_login'] = visited_follow_login

    return visited_user, tweet_list, following_list, follower_list

def get_original_tweet(tweet):
    original_tweet = tweet
    if tweet.original_tweet:
        original_tweet = Tweet.objects.get(pk=tweet.original_tweet.id)
    return original_tweet

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
