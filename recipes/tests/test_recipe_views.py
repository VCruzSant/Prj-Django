# from unittest import skip

from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
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

        self.assertEqual(response_recipes.first().title, 'Recipe Title test')

    def test_recipe_home_template_not_published_dont_load_recipe(self):
        # If not is_published, dont show
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No Recipes Found', response.content.decode('utf-8'))

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                               kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_context_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        response_recipes = response.context['recipes']

        self.assertEqual(response_recipes[0].title, 'Recipe Title test')

    def test_recipe_category_template_not_published_dont_load_recipe(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={
                    'id': recipe.category.id})  # type: ignore
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

    def test_recipe_detail_template_not_published_dont_load_recipe(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={
                    'id': recipe.id})  # type: ignore
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_context_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        response_recipes = response.context['recipe']
        self.assertEqual(response_recipes.title, 'Recipe Title test')

    def test_recipe_search_load_correct_view(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_context_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_404_if_no_input_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)
