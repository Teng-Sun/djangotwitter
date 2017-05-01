from .base import *


@login_required
def retweet(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    user = request.user

    original_tweet = get_original_tweet(tweet)

    if not Tweet.objects.filter(author=user, original_tweet=original_tweet):
        
        original_tweet.retweet_num += 1
        original_tweet.save()

        new_tweet = create_tweet(user, original_tweet.content, original_tweet)
        create_notification(user, tweet.author, 'R', new_tweet)
        cretae_streams(new_tweet, 'R')

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
        reply_form = TweetForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)

            reply = create_tweet(user, new_reply.content, original_tweet=None)
            replyship = Replyship(
                tweet = original_tweet,
                reply = reply,
                tweet_user = original_tweet.author,
                reply_user = user,
            )
            replyship.save()

            tweet.reply_num += 1
            tweet.save()

            create_notification(user, tweet.author, 'T', reply)

            cretae_streams(reply, 'Y')
    else:
        reply_form = TweetForm()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def like(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    original_tweet = get_original_tweet(tweet)
    user = request.user
    if not Like.objects.filter(tweet=original_tweet, author=user):
        new_like = Like(
            author = user,
            tweet = original_tweet,
        )
        new_like.save()
        original_tweet.like_num += 1
        original_tweet.save()

        create_notification(user, tweet.author, 'L', tweet)
        usernames = search_username(tweet.content)
        notificate_users(usernames, user, 'L', tweet)

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unlike(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    original_tweet = get_original_tweet(tweet)
    user = request.user
    like = Like.objects.get(tweet=original_tweet, author=user)
    if like:
        like.delete()
        original_tweet.like_num -= 1
        original_tweet.save()

        Notification.objects.filter(
            initiative_user = user,
            notificate_type = 'L',
            tweet = tweet
        ).delete()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    if tweet and tweet.author == request.user:
        original_tweet = get_original_tweet(tweet)
        replyship = Replyship.objects.filter(reply=original_tweet)
        if replyship:
            replyship[0].tweet.reply_num -= 1
            replyship[0].tweet.save()
        original_tweet.delete()
    
    return redirect(request.META.get('HTTP_REFERER'))