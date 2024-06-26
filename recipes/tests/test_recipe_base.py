from django.test import TestCase

from recipes.models import Recipe, Category, User


class RecipeTestBase(TestCase):
    def setUp(self):
        return super().setUp()

    def make_category(self, name=Category):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='User',
        last_name='Name',
        username='username',
        password='123456',
        email='user@email.com',
    ):
        return User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
            self,
            category_data=None,
            author_data=None,
            title='Recipe Title test',
            description='Recipe Description',
            slug='recipe-slug-test-1',
            preparation_time=1,
            preparation_time_unit='Hour',
            servings='3',
            servings_unit='Portions',
            preparation_step='Recipe preparation step',
            preparation_step_is_html=False,
            is_published=True,
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(  # noqa:F841
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
        )
