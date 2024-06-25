from django.core.exceptions import ValidationError

from parameterized import parameterized

from .test_recipe_base import RecipeTestBase, Recipe


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self) -> Recipe:
        recipe = Recipe(
            category=self.make_category(name='Test Default'),  # type: ignore
            author=self.make_author(username='newuser'),
            title='Recipe Title test',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=1,
            preparation_time_unit='Hour',
            servings='3',
            servings_unit='Portions',
            preparation_step='Recipe preparation step',
        )

        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_fields_has_raises_if_title_have_more_65_chars(self):
        self.recipe.title = 'A' * 70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_lenth(self, field, max_lenth):
        setattr(self.recipe, field, 'A' * (max_lenth + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_fale_by_default(self) -> None:
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.preparation_step_is_html)

    def test_recipe_is_published_is_fale_by_default(self) -> None:
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        self.recipe.title = 'Test Representation'
        self.assertEqual(str(self.recipe), 'Test Representation')
