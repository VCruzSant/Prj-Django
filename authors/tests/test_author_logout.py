from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_try_logout_with_get_method(self):
        User.objects.create_user(username='usertest', password='userpass')

        self.client.login(username='usertest', password='userpass')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
        )

    def test_user_try_logout_another_user(self):
        User.objects.create_user(username='usertest', password='userpass')

        self.client.login(username='usertest', password='userpass')

        response = self.client.post(
            reverse('authors:logout'), data={
                'username': 'another_user'
            }, follow=True)

        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8')
        )

    def test_user_logout_successfully(self):
        User.objects.create_user(username='usertest', password='userpass')

        self.client.login(username='usertest', password='userpass')

        response = self.client.post(
            reverse('authors:logout'), data={
                'username': 'usertest'
            }, follow=True)

        self.assertIn(
            'Logged out successfully',
            response.content.decode('utf-8')
        )
