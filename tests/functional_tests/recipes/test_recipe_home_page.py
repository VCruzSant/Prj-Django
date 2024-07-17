import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_page_without_recipe_not_found(self):
        self.browser.get(self.live_server_url)
        self.sleep()

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No Recipes Found', body.text)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_search_input_find_correct_recipe(self):
        recipe = self.make_recipe_batch()
        title_needed = 'A Recipe'
        recipe[0].title = title_needed
        recipe[0].save()
        # User open the page
        self.browser.get(self.live_server_url)

        # See a search fiel with text "A Recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a Recipe..."]'
        )

        # Click in this input and digit "Recipe Title 0"
        search_input.send_keys(recipe[0].title)
        search_input.send_keys(Keys.ENTER)

        self.sleep()

        # see recipe with title "A Recipe"
        self.assertIn(
            title_needed, self.browser.find_element(
                By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.recipe_list_view.PER_PAGE', new=3)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_batch(20)

        # User open the page
        self.browser.get(self.live_server_url)

        self.sleep(4)
        # see pagination and click
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # See more 3 Recipes
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            3
        )
