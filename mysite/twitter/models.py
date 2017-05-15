from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Tweet(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    created_date = models.DateTimeField(
        default = timezone.now
    )
    original_tweet = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank = True,
    )
    retweet_num = models.IntegerField(default=0)
    like_num = models.IntegerField(default=0)
    reply_num = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_date']


class Replyship(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        related_name='be_replied_tweet',
        on_delete=models.CASCADE
    )
    reply = models.ForeignKey(
        Tweet,
        related_name='reply_tweet',
        on_delete=models.CASCADE
    )
    tweet_user = models.ForeignKey(
        User,
        related_name='be_replied_user',
    )
    reply_user = models.ForeignKey(
        User,
        related_name='reply_user',
        on_delete=models.CASCADE,
    )

    reply_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-reply_date']


class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-like_date']

class Followship(models.Model):
    followed_user = models.ForeignKey(
        User,
        related_name='followings', 
        on_delete=models.CASCADE,
    )
    initiative_user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
    )
    date_follow = models.DateTimeField(default=timezone.now)

class Notification(models.Model):
    MENTION = 'M'
    REPLY = 'Y'
    RETWEET = 'R'
    RETWEET_MENTION = 'RM'
    LIKE = 'L'
    LIKE_MENTION = 'LM'
    FOLLOW = 'F'

    NOTIFY_TYPE = [
        (MENTION, 'mention'),
        (REPLY, 'reply'),
        (RETWEET, 'retweet'),
        (RETWEET_MENTION, 'retweet_mention'),
        (LIKE, 'like'),
        (LIKE_MENTION, 'like_mention'),
        (FOLLOW, 'follow'),
    ]

    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        null=True,
        blank = True,
    )
    notify_user = models.ForeignKey(
        User,
        related_name='notify_user',
        on_delete=models.CASCADE,
        null=True,
        blank = True,
    )
    notified_user = models.ForeignKey(
        User,
        related_name='notified_user',
        on_delete=models.CASCADE,
        null=True,
        blank = True,
    )
    notified_type = models.CharField(
        max_length = 1,
        choices = NOTIFY_TYPE,
        default = REPLY,
        null=True,
        blank = True,
    )
    notify_date = models.DateTimeField(
        default = timezone.now
    )
    class Meta:
        ordering = ['-notify_date']


class Stream(models.Model):
    TWEET = 'T'
    REPLY = 'Y'
    RETWEET = 'R'

    STREAM_TYPE = [
        (TWEET, 'tweet'),
        (REPLY, 'reply'),
        (RETWEET, 'retweet'),
    ]

    receiver = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )
    tweet = models.ForeignKey(
        Tweet,
        on_delete = models.CASCADE,
    )
    stream_type = models.CharField(
        max_length = 1,
        choices = STREAM_TYPE,
        default = TWEET
    )
    stream_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-stream_date']

    def __str__(self):
        return str(self.receiver)
