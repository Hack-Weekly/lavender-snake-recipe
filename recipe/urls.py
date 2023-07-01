from django.urls import path
from recipe.views import (
                            RecipeListView,
                            RecipeCreatView,
                            RecipeUpdateView,
                            RecipeDeleteView,
                            RecipeDetailView,
                        )
app_name = 'recipe'

urlpatterns = [
    path('', RecipeListView.as_view(),name='recipelist'),
    path('create/', RecipeCreatView.as_view(),name='recipecreate'),
    path('<slug:slug>/', RecipeDetailView.as_view(),name='recipedetail'),
    path('<slug:slug>/update', RecipeUpdateView.as_view(),name='recipeupdate'),
    path('<slug:slug>/delete', RecipeCreatView.as_view(),name='recipedelete'),
]