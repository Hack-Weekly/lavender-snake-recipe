from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from recipe.models import Recipe, Tag

class RecipeListAPIViewTest(APITestCase):

    def setUp(self):

        

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')
        self.recipe1 = Recipe.objects.create(
            author=self.user,
            title='Recipe 1',
            ingredients='Ingredient 1, Ingredient 2',
            servings=4,
            prep_time=30,
            instructions='Step 1, Step 2, Step 3'
        )
        self.recipe1.tags.add(self.tag1)
        self.recipe2 = Recipe.objects.create(
            author=self.user,
            title='Recipe 2',
            ingredients='Ingredient 1, Ingredient 2',
            servings=4,
            prep_time=30,
            instructions='Step 1, Step 2, Step 3'
        )
        self.recipe2.tags.add(self.tag2)

    def test_get_recipe_list(self):
        url = reverse('api:recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming pagination is used
        self.assertEqual(response.data['results'][0]['title'], 'Recipe 1')
        self.assertEqual(response.data['results'][1]['title'], 'Recipe 2')

    def test_post_recipe(self):
        url = reverse('api:recipe-list')
        data = {
            'title': 'New Recipe',
            'author': self.user.pk,
            'ingredients': 'Ingredient 1, Ingredient 2',
            'servings': 4,
            'prep_time': 30,
            'instructions': 'Step 1, Step 2, Step 3',
            'tags': [self.tag1.pk, self.tag2.pk]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 3)  

        recipe = Recipe.objects.get(title='New Recipe')
        self.assertEqual(recipe.author, self.user)
        self.assertEqual(recipe.ingredients, 'Ingredient 1, Ingredient 2')
        self.assertEqual(recipe.servings, 4)
        self.assertEqual(recipe.prep_time, 30)
        self.assertEqual(recipe.instructions, 'Step 1, Step 2, Step 3')
        self.assertIn(self.tag1, recipe.tags.all())
        self.assertIn(self.tag2, recipe.tags.all())



class RecipeDetailAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Recipe 3',
            ingredients='Ingredient 1, Ingredient 2',
            servings=4,
            prep_time=30,
            instructions='Step 1, Step 2, Step 3'
        )
        self.recipe.tags.add(self.tag1)

    def test_get_recipe_detail(self):
        url = reverse('api:recipe_detail', args=[self.recipe.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['recipe']['title'], 'Recipe 3')
        self.assertEqual(response.data['recipe']['author']['username'], 'testuser')
        self.assertIn(self.tag1.pk, [tag['id'] for tag in response.data['recipe']['tags']])

    def test_put_recipe(self):
        url = reverse('api:recipe_detail', args=[self.recipe.slug])
        data = {
            'title': 'Updated Recipe',
            'author': self.user.pk,
            'ingredients': 'Updated Ingredient 1, Updated Ingredient 2',
            'servings': 6,
            'prep_time': 45,
            'instructions': 'Updated Step 1, Step 2, Step 3',
            'tags': [self.tag1.pk, self.tag2.pk]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Updated Recipe')
        self.assertEqual(self.recipe.ingredients, 'Updated Ingredient 1, Updated Ingredient 2')
        self.assertEqual(self.recipe.servings, 6)
        self.assertEqual(self.recipe.prep_time, 45)
        self.assertEqual(self.recipe.instructions, 'Updated Step 1, Step 2, Step 3')
        self.assertIn(self.tag1, self.recipe.tags.all())
        self.assertIn(self.tag2, self.recipe.tags.all())

    def test_delete_recipe(self):
        url = reverse('api:recipe_detail', args=[self.recipe.slug])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())


class RecipeSearchAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        #self.recipe1 = Recipe.objects.create(title='Pasta Recipe', author=self.user, ingredients='Pasta, Sauce')
        self.recipe1=Recipe.objects.create(
            author=self.user,
            title='Pasta Recipe',
            ingredients='Pasta, Sauce',
            servings=4,
            prep_time=30,
            instructions='Step 1, Step 2, Step 3'
        )
        #self.recipe2 = Recipe.objects.create(title='Pizza Recipe', author=self.user, ingredients='Dough, Cheese')
        self.recipe2 = Recipe.objects.create(
            author=self.user,
            title='Pizza Recipe',
            ingredients='Dough, Cheese',
            servings=4,
            prep_time=30,
            instructions='Step 1, Step 2, Step 3'
        )

    def test_search_recipes(self):
        url = reverse('api:recipe-search')
        response = self.client.get(url, {'query': 'pasta'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pasta Recipe')

        response = self.client.get(url, {'query': 'recipe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Pasta Recipe')
        self.assertEqual(response.data[1]['title'], 'Pizza Recipe')

    def test_search_recipes_no_query(self):
        url = reverse('api:recipe-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



