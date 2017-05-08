from .share import *

def profile_subnav_title(request, username):
    visited_user = User.objects.get(username=username)
    tweet_num = len(Tweet.objects.filter(author=visited_user, original_tweet__isnull=True))
    following_num = len(Followship.objects.filter(initiative_user=visited_user))
    follower_num = len(Followship.objects.filter(followed_user=visited_user))
    like_num = len(Like.objects.filter(author=visited_user))

    return visited_user, tweet_num, following_num, follower_num, like_num

def set_profile_subnav_session(request, username):
    login_user = request.user
    visited_user, tweet_num, following_num, \
        follower_num, like_num = profile_subnav_title(request, username)

    request.session['tweet_num'] = tweet_num
    request.session['following_num'] = following_num
    request.session['follower_num'] = follower_num
    request.session['like_num'] = like_num
    request.session['login_follow_visited'] = bool(check_followship(login_user, visited_user))
    request.session['visited_follow_login'] = bool(check_followship(visited_user, login_user))
    return visited_user