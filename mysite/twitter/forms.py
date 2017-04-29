from django import forms

from django.contrib.auth.models import User
from .models import Tweet


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ('content',)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('content',)