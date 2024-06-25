from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category(
            name='Category Test'  # type: ignore
        )
        return super().setUp()

    def test_recipe_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_recipe_category_has_raises_if_title_have_more_65_chars(self):
        self.category.name = 'A' * 66

        with self.assertRaises(ValidationError):
            self.category.full_clean()
