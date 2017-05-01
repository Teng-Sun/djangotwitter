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
    notificate_type = (
        ('L', 'like'),
        ('T', 'tweet'),
        ('R', 'retweet'),
        ('F', 'Follow')
    )

    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        null=True,
        blank = True,
    )
    initiative_user = models.ForeignKey(
        User,
        related_name='notificate_user',
        on_delete=models.CASCADE,
    )
    notificated_user = models.ForeignKey(
        User,
        related_name='notificated_user',
        on_delete=models.CASCADE,
    )
    notificate_type = models.CharField(
        max_length = 1,
        choices = notificate_type,
        default = 'T'
    )
    notificate_date = models.DateTimeField(
        default = timezone.now
    )
    class Meta:
        ordering = ['-notificate_date']

