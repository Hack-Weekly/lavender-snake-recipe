from django.test import TestCase
from django.urls import reverse, resolve
from api.views import (
    MyTokenObtainPairView,
    RegisterView,
    testEndPoint,
    DocsView,
    RecipeListAPIView,
    RecipeDetailAPIView,
    UserFavouriteAPIView,
    RecipeSearchAPIView,
    UserHistoryAPIView,
    TagAPIView,
    UserProfileAPIView,
    getRoutes,
)

class UrlsTestCase(TestCase):
    def test_token_url(self):
        url = reverse('api:token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, MyTokenObtainPairView)

    def test_token_refresh_url(self):
        url = reverse('api:token_refresh')
        self.assertEqual(resolve(url).func.view_class.__name__, 'TokenRefreshView')

    def test_register_url(self):
        url = reverse('api:auth_register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_test_endpoint_url(self):
        url = reverse('api:test')
        self.assertEqual(resolve(url).func, testEndPoint)

    def test_docs_url(self):
        url = reverse('api:docs')
        self.assertEqual(resolve(url).func.view_class, DocsView)

    def test_recipe_list_url(self):
        url = reverse('api:recipe-list')
        self.assertEqual(resolve(url).func.view_class, RecipeListAPIView)

    def test_recipe_detail_url(self):
        url = reverse('api:recipe_detail', args=['recipe-slug'])
        self.assertEqual(resolve(url).func.view_class, RecipeDetailAPIView)

    def test_recipe_favourite_url(self):
        url = reverse('api:recipe_favourite', args=['recipe-slug'])
        self.assertEqual(resolve(url).func.view_class, UserFavouriteAPIView)

    def test_recipe_search_url(self):
        url = reverse('api:recipe-search')
        self.assertEqual(resolve(url).func.view_class, RecipeSearchAPIView)

    def test_user_history_url(self):
        url = reverse('api:recipe-history')
        self.assertEqual(resolve(url).func.view_class, UserHistoryAPIView)

    def test_user_favourite_url(self):
        url = reverse('api:user_favourite')
        self.assertEqual(resolve(url).func.view_class, UserFavouriteAPIView)

    def test_tags_url(self):
        url = reverse('api:tags')
        self.assertEqual(resolve(url).func.view_class, TagAPIView)

    def test_profile_url(self):
        url = reverse('api:profile')
        self.assertEqual(resolve(url).func.view_class, UserProfileAPIView)

    def test_default_url(self):
        url = reverse('api:routes')
        self.assertEqual(resolve(url).func, getRoutes)
