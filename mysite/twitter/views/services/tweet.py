from .share import *

def create_tweet(author, content, original_tweet):
    new_tweet = Tweet(
        author = author,
        content = content,
        original_tweet = original_tweet,
    )
    new_tweet.save()
    return new_tweet

def get_original_tweet(tweet):
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

def get_tweet_data(tweet, visited_user, login_user):
    original_tweet = get_original_tweet(tweet)
    tweet.retweet_num = original_tweet.retweet_num
    tweet.like_num = original_tweet.like_num
    tweet.reply_num = original_tweet.reply_num
    if Like.objects.filter(author=login_user, tweet=original_tweet):
        tweet.has_been_liked = True
    if Tweet.objects.filter(author=login_user, original_tweet=original_tweet):
        tweet.has_been_retweeded = True
    tweet.replies_list = []
    get_tweet_replies(tweet, tweet.replies_list)
    return tweet
   
def get_show_tweets(tweet_list, visited_user, login_user):
    show_tweets = list(tweet_list)
    for tweet in tweet_list:
        get_tweet_data(tweet, visited_user, login_user)
        if Tweet.objects.filter(author=visited_user, original_tweet=tweet):
            show_tweets.remove(tweet)
    return show_tweets

def get_show_likes(likes, login_user):
    show_tweets = []
    for like in likes:
        tweet = like.tweet

        tweet.replies_list = []
        get_tweet_replies(tweet, tweet.replies_list)

        if Like.objects.filter(author=login_user, tweet=tweet):
            tweet.has_been_liked = True
        if Tweet.objects.filter(author=login_user, original_tweet=tweet):
            tweet.has_been_retweeded = True

        show_tweets.append(tweet)
    return show_tweets