from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['last_name'], 'Your Last Name')

    username = forms.CharField(
        required=True,
        label='Username',
        error_messages={
            'required': 'This field must not be empty',
            'invalid': 'This field is invalid',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have last less than 150 characters',
        },
        min_length=4, max_length=150,
    )

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

    email = forms.CharField(
        label='E-mail',
        error_messages={
            'required': 'Must be valid',
        },
        help_text='Must be valid'
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
            'first_name': 'First name',
            'last_name': 'Last name',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('User e-mail already exists', code='invalid')

        return email

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
