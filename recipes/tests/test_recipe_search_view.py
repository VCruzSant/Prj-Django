# from unittest import skip

from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_load_correct_view(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_context_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_404_if_no_input_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_scaped(self):
        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertIn('Search for &quot;test&quot;',
                      response.content.decode('utf-8'))
