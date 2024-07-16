from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils import django_forms, strings


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        django_forms.add_attr(self.fields.get(
            'preparation_step'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = (
            'title', 'description', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_step', 'cover',
        )
        widgets = {
            "cover": forms.FileInput(attrs={'class': 'span-2'}),
            "servings_unit": forms.Select(choices=(
                ('Portions', 'Portions'),
                ('Pieces', 'Pieces'),
                ('People', 'People'),
            )),
            "preparation_time_unit": forms.Select(choices=(
                ('Minutes', 'Minutes'),
                ('Hours', 'Hours'),
            ))
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if description == title:
            self._my_errors['description'].append(
                'description should not be the same as the title'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        field_name = 'title'
        field_message = 'Must have be positive number'

        field_value = self.cleaned_data.get(field_name)

        if len(field_value) < 5:  # type: ignore
            self._my_errors[field_name].append(field_message)
        return field_value

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_message = 'Must have be positive number'

        field_value = self.cleaned_data.get(field_name)

        if not strings.is_positive_number(self.cleaned_data.get(field_name)):
            self._my_errors[field_name].append(field_message)
        return field_value
