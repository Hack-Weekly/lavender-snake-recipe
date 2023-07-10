from django.urls import path
from api import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('test/', views.testEndPoint, name='test'),
    path('docs/', views.DocsView.as_view(), name='docs'),
    path('recipes/', views.RecipeListAPIView.as_view(), name='recipe-list'),
    path('recipe/<slug:slug>/', views.RecipeDetailAPIView.as_view(), name='recipe-detail'),
    path('search/', views.RecipeSearchAPIView.as_view(), name='recipe-search'),
    path('history/', views.UserHistoryAPIView.as_view(), name='recipe-history'),

    path('', views.getRoutes)
]