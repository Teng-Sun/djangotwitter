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
    is_retweet = models.BooleanField(default=False)
    retweet_num = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_date']

class Reply(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        related_name="reply_user",
        on_delete=models.CASCADE,
        default='',
        null=True,
    )
    content = models.TextField()
    reply_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-reply_date']

class Retweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(User, )
    retweet_date =  models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-retweet_date']

class Retweetship(models.Model):
    original_tweet = models.ForeignKey(
        Tweet,
        related_name='original',
        on_delete=models.CASCADE
    )
    re_tweet = models.ForeignKey(
        Tweet,
        related_name='re',
        on_delete=models.CASCADE,
    )
    re_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-re_date']


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

