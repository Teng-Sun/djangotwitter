from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from twitter.views.services import profile_nav

class ProfileTest(TestCase):
    fixtures = [
        'twitter/fixtures/test_user_data.json',
        'twitter/fixtures/test_followship_data.json',
    ]

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')

    def test_check_followship(self):
        admin_follows_user1 = profile_nav.check_followship(self.admin, self.user1)
        user1_follows_admin = profile_nav.check_followship(self.user1, self.admin)
        self.assertTrue(user1_follows_admin)
        self.assertFalse(admin_follows_user1)

    def test_set_sessions(self):
        data = [
            ('a', 1),
            ('b', 2)
        ]
        c = Client()
        response = c.get('/profile/admin')
        request = response.wsgi_request
        profile_nav.set_sessions(request, data)
        self.assertEqual(request.session['a'], 1)
        self.assertEqual(request.session['b'], 2)