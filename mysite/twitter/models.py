from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Following(models.Model):
    username = models.CharField(max_length=200)
    joined_date = models.DateTimeField()
    bio = models.TextField()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['joined_date']

class Tweet(models.Model):
    author = models.ForeignKey(Following)
    context = models.TextField()
    created_date = models.DateTimeField(
        default = timezone.now
    )

    def __str__(self):
        return self.author

    class Meta:
        ordering = ['-created_date']


