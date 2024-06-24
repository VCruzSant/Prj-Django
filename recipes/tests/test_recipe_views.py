from django.test import TestCase
from django.urls import reverse, resolve

from recipes import views
from recipes.models import Recipe, Category, User


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIs(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_recipe_not_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No Recipes Found', response.content.decode('utf-8'))

    def test_recipe_home_context_loads_recipes(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create(
            first_name='User',
            last_name='Name',
            username='username',
            password='123456',
            email='user@email.com',
        )

        recipe = Recipe.objects.create(  # noqa:F841
            category=category,
            author=author,
            title='Recipe Title test',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=1,
            preparation_time_unit='Hour',
            servings='3',
            servings_unit='Portions',
            preparation_step='Recipe preparation step',
            preparation_step_is_html=False,
            is_published=True,
        )

        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']

        self.assertEqual(response_recipes.first().title, 'Recipe Title test')

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                               kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)
