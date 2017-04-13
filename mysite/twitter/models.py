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

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_date']

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

