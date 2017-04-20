from django import forms

from django.contrib.auth.models import User
from .models import Tweet, Followship, Reply


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ('content',)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class FollowForm(forms.ModelForm):
    class Meta:
        model = Followship
        fields = ()

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('content',)