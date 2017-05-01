from .handler import *

def index(request):
    user = request.user
    stream_list = []
    if user.is_authenticated():
        streams = Stream.objects.filter(receiver=user)
        for stream in streams:
            get_tweet_data(stream.tweet, user, user)
        paginate_by = 10
        stream_list = pagination(request, streams, paginate_by)
    return render(request, 'twitter/index.html', {
        'stream_list': stream_list,
        'object_list': stream_list,
    })

def notification(request):
    user = request.user
    notifications = Notification.objects.filter(notificated_user=user)
    for notification in notifications:
        tweet = notification.tweet
        if tweet:
            get_tweet_data(tweet, user, user)
        notification.subtitle = get_notification_subtitle(notification.notificate_type, tweet)

    paginate_by = 10
    notification_list = pagination(request, notifications, paginate_by)

    return render(request, 'twitter/notification.html', {
        'notification_list': notification_list,
        'object_list': notification_list,
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


def profile(request, username):
    visited_user = set_profile_subnav_session(request, username)
    tweet_list = list(Tweet.objects.filter(author=visited_user))
    show_tweets = get_show_tweets(tweet_list, visited_user, request.user)

    paginate_by = 10

    tweets = pagination(request, show_tweets, paginate_by)
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
            new_tweet = create_tweet(request.user, tweet.content, original_tweet=None)
            cretae_streams(new_tweet, 'T')
            return redirect('profile', username=request.user.username)
    else:
        form = TweetForm()
    return render(request, 'twitter/post_tweet.html', {
        'form': form,
    })

def following(request, username):
    visited_user = User.objects.get(username=username)
    following_list = Followship.objects.filter(initiative_user=visited_user)
    paginate_by = 10
    followings = pagination(request, following_list, paginate_by)
    return render(request, 'twitter/following.html', {
        'visited_user': visited_user,
        'followings': followings,
        'object_list': followings,
    })

def follower(request, username):
    visited_user = User.objects.get(username=username)
    follower_list = Followship.objects.filter(followed_user=visited_user)
    paginate_by = 10
    followers = pagination(request, follower_list, paginate_by)
    return render(request, 'twitter/follower.html', {
        'visited_user': visited_user,
        'followers': followers,
        'object_list': followers,
    })

@login_required
def likes(request, username):
    visited_user = User.objects.get(username=username)
    likes = Like.objects.filter(author=visited_user) or []
    show_likes = get_show_likes(likes, request.user)
    paginate_by = 10
    like_list = pagination(request, show_likes, paginate_by)

    return render(request, 'twitter/likes.html', {
        'visited_user': visited_user,
        'tweets': like_list,
        'object_list': like_list,
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
            create_notification(login_user, visited_user, 'F', tweet=None)
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