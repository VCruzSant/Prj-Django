# from unittest import skip

from django.urls import reverse, resolve
from unittest.mock import patch

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    # @skip('WIP(work in progress)')
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
        # Force test fail to implement in future
        # self.fail()

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
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']
        ...
        self.assertEqual(response_recipes[0].title, 'Recipe Title test')

    def test_recipe_home_template_not_published_dont_load_recipe(self):
        # If not is_published, dont show
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No Recipes Found', response.content.decode('utf-8'))

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_view_load_pagination(self):
        for i in range(9):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug': f'r{i}'}
            self.make_recipe(**kwargs)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
