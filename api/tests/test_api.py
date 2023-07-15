from django.test import TestCase
from users.models import User
from recipe.models import Recipe, Tag

class RecipeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag = Tag.objects.create(name='Tag1')

    def test_recipe_model(self):
        recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            ingredients='Ingredient 1, Ingredient 2',
            servings=4,
            prep_time=30,
            instructions='Step 1, Step 2, Step 3'
        )
        recipe.tags.add(self.tag)

        self.assertEqual(recipe.title, 'Test Recipe')
        self.assertEqual(recipe.author, self.user)
        self.assertEqual(recipe.ingredients, 'Ingredient 1, Ingredient 2')
        self.assertEqual(recipe.servings, 4)
        self.assertEqual(recipe.prep_time, 30)
        self.assertEqual(recipe.instructions, 'Step 1, Step 2, Step 3')
        self.assertIn(self.tag, recipe.tags.all())
        self.assertIsNotNone(recipe.slug)
