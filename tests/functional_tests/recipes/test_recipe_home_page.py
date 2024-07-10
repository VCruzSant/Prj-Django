import pytest
from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipe_not_found(self):
        self.browser.get(self.live_server_url)
        self.sleep()

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No Recipes Found', body.text)
