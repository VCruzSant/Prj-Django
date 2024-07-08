import re
from django.core.exceptions import ValidationError


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
