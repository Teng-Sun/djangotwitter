# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 04:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followship',
            old_name='date_following',
            new_name='date_follow',
        ),
        migrations.RenameField(
            model_name='followship',
            old_name='following',
            new_name='followed_user',
        ),
        migrations.RenameField(
            model_name='followship',
            old_name='follower',
            new_name='initiative_user',
        ),
    ]