# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 00:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0010_auto_20170425_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retweet',
            name='author',
        ),
        migrations.RemoveField(
            model_name='retweet',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='retweetship',
            name='original_tweet',
        ),
        migrations.RemoveField(
            model_name='retweetship',
            name='re_tweet',
        ),
        migrations.AddField(
            model_name='tweet',
            name='retweet_num',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Retweet',
        ),
        migrations.DeleteModel(
            name='Retweetship',
        ),
    ]
