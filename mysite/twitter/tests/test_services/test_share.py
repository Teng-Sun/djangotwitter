from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from twitter.views.services import share
from twitter.models import Notification, Tweet


