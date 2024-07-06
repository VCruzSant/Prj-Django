from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(
        r'^(?=.*[a-z])'
        r'(?=.*[A-Z])'
        r'(?=.*[0-9])'
        r'(?=.*[ -\/:-@[-`{-~])'
        r'.{6,}'
        r'$',
        flags=re.M
    )

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter, '
            'password must contain at least one number, '
            'must contain at least one special character (e.g., !@#$%^&*)'
        ),
            code='Invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['last_name'], 'Your Last Name')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password here'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter, '
            'password must contain at least one number, '
            'must contain at least one special character (e.g., !@#$%^&*)'
        ),
        validators=[strong_password],
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password here'
            }
        ),
        label='Confirm Password',
        error_messages={
            'required': 'Password must not be empty'
        }

    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'Must be valid'
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
                'invalid': 'This field is invalid,'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here'
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError(
                {
                    'password': 'Password and Confirm password must be equal',
                    'password2': 'Password and Confirm password must be equal'
                }

            )
