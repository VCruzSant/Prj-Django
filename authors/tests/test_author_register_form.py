from django.test import TestCase as DjangoTestCase
from django.urls import reverse

from authors.forms import RegisterForm
from unittest import TestCase
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Type your username here'),
        ('password', 'Type your password here'),
        ('password2', 'Confirm your password here'),
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('last_name', 'Your Last Name'),
    ])
    def test_fields_placeholder_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current, needed)

    @parameterized.expand([
        ('password', 'Password must have at least one uppercase letter, '
                     'one lowercase letter, '
                     'password must contain at least one number, '
         'must contain at least one special character (e.g., !@#$%^&*)'
         ),
        ('email', 'Must be valid'),
    ])
    def test_fields_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text

        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Confirm Password'),
    ])
    def test_fields_label_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label

        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'User',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@test.com',
            'password': 'Str@0ngPass',
            'password2': 'Str@0ngPass',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('email', 'Must be valid'),
        ('password', 'Password must not be empty'),
        ('password2', 'Password must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_lenght_should_be_150(self):
        self.form_data['username'] = 'vin'
        msg = 'Username must have at least 4 characters'
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_lenght_should_be_4(self):
        self.form_data['username'] = 'v' * 151
        msg = 'Username must have last less than 150 characters'
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_should_be_strong(self):
        self.form_data['password'] = 'abcdef'
        msg = 'Password must have at least one uppercase letter, '
        'one lowercase letter, '
        'password must contain at least one number, '
        'must contain at least one special character (e.g., !@#$%^&*)'
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_confirmation_are_equal(self):
        self.form_data['password'] = 'Str@0ngPass'
        self.form_data['password2'] = 'Str@0ngPassw'
        msg = 'Password and Confirm password must be equal'
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_register_view_return_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url, self.form_data, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_email_already_exists(self):
        self.client.post(
            reverse('authors:register_create'),
            self.form_data,
            follow=True
        )

        response = self.client.post(
            reverse('authors:register_create'),
            self.form_data,
            follow=True
        )

        self.assertIn(
            'User e-mail already exists',
            response.content.decode('utf-8')
        )

        self.assertIn(
            'User e-mail already exists',
            response.context['form'].errors.get('email')
        )

    def test_author_can_login(self):
        self.client.post(
            reverse('authors:register_create'),
            self.form_data,
            follow=True
        )

        is_authenticated = self.client.login(
            username='User',
            password='Str@0ngPass'
        )

        self.assertTrue(is_authenticated)
