from authors.forms import RegisterForm
from django.test import TestCase
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
