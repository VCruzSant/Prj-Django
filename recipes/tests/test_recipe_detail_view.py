# from unittest import skip

from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
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
