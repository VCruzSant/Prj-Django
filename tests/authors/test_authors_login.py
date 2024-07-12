from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_data_valid_sucessfully(self):
        user = User.objects.create_user(username="usertest", password="pass")

        # User open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User see login form
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )
        username_field = self.get_by_placeholder(form, 'Type your Username')
        password_field = self.get_by_placeholder(form, 'Type your Password')

        # User digit your username and pass
        username_field.send_keys(user.username)
        password_field.send_keys('pass')
        form.submit()

        # user see login sucess message
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(
            f'You are logged with {user.username}', body
        )
