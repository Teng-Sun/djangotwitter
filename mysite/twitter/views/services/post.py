from twitter.models import Tweet, Replyship, Like
from copy import deepcopy

def create_tweet(author, content, original_tweet):
    new_tweet = Tweet(
        author = author,
        content = content,
        original_tweet = original_tweet,
    )
    new_tweet.save()
    return new_tweet

def get_action_data(tweet, user):
    original_tweet = get_original(tweet)

    tweet.retweet_num = original_tweet.retweet_num
    tweet.like_num = original_tweet.like_num
    tweet.reply_num = original_tweet.reply_num

    tweet.replies_list = []
    get_tweet_replies(original_tweet, tweet.replies_list)
    if user.is_authenticated():
        tweet.has_been_liked = been_liked(original_tweet, user)
        tweet.has_been_retweeded = been_retweeted(original_tweet, user)
    else:
        tweet.has_been_liked = False
        tweet.has_been_retweeded = False

def show_tweets(tweet_list, visited_user, login_user):
    tweets = []
    for tweet in tweet_list:
        get_action_data(tweet, login_user)
        if not been_retweeted(tweet, visited_user):
            tweets.append(tweet)
    return tweets

def show_like_tweets(likes, user):
    show_tweets = []
    for like in likes:
        tweet = like.tweet
        get_action_data(tweet, user)
        show_tweets.append(tweet)
    return show_tweets

def get_original(tweet):
    return tweet.original_tweet or tweet

def get_reply_replies(reply, reply_list):
    replyships = Replyship.objects.filter(tweet=reply)
    for replyship in replyships:
        new_reply = replyship.reply
        reply_list.append(new_reply)
        get_reply_replies(new_reply, reply_list)

def get_tweet_replies(tweet, replies_list):
    replyships = Replyship.objects.filter(tweet=tweet)
    for index, replyship in enumerate(replyships):
        reply = replyship.reply
        reply_list = [reply]
        get_reply_replies(reply, reply_list)
        replies_list.append([])
        replies_list[index] = reply_list

def been_retweeted(tweet, user):
    return bool(Tweet.objects.filter(author=user, original_tweet=tweet))

def been_liked(tweet, user):
    return bool(Like.objects.filter(tweet=tweet, author=user))

def max_index(tweets, field_name):
    num = 0
    selected_index = 0
    for index, t in enumerate(tweets):
        count = getattr(t, field_name)
        if count > num:
            num = count
            selected_index = index
    return selected_index

def select_tweet(tweets, field_name, login_user, results):
    if tweets:
        selected_index = max_index(tweets, field_name)
        tweet = tweets[selected_index]
        get_action_data(tweet, login_user)
        results.append(tweet)