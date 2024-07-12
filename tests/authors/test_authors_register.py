from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 10)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@dummy.com')

        callback(form)
        return form

    def test_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(
                form, 'Type your username here'
            )
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('This field must not be empty', form.text)

        self.form_field_test_with_callback(callback)

    def test_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(
                form, 'Your Last Name'
            )
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('This field must not be empty', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(
                form, 'Your username'
            )
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('This field must not be empty', form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(
                form, 'Your e-mail'
            )
            email_field.send_keys('emailinvalid@')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('Must be valid', form.text)

        self.form_field_test_with_callback(callback)

    def test_password_not_match_error_message(self):
        def callback(form):
            password_field1 = self.get_by_placeholder(
                form, 'Type your password here'
            )
            password_field2 = self.get_by_placeholder(
                form, 'Confirm your password here'
            )
            password_field1.send_keys('P@ssword1')
            password_field2.send_keys('P@ssword12')

            password_field2.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(
                'Password and Confirm password must be equal', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_register_success(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(
            form, 'Type your username here'
        ).send_keys('First')

        self.get_by_placeholder(
            form, 'Your Last Name'
        ).send_keys('Last')

        self.get_by_placeholder(
            form, 'Your username'
        ).send_keys('username')

        self.get_by_placeholder(
            form, 'Your e-mail'
        ).send_keys('test@selenium.com')

        self.get_by_placeholder(
            form, 'Type your password here'
        ).send_keys('P@ssword1')

        self.get_by_placeholder(
            form, 'Confirm your password here'
        ).send_keys('P@ssword1')

        form.submit()
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Your User is create, please log in', body)
