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
