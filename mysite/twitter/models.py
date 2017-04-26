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

class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(User)
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