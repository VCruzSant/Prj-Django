# from unittest import skip

from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
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
