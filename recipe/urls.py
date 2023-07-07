from django.urls import path
from recipe.views import (
                            RecipeListView,
                            RecipeCreatView,
                            RecipeUpdateView,
                            RecipeDeleteView,
                            RecipeDetailView,
                            RecipeSearchView,
                            UserHistoryView,
                        )
app_name = 'recipe'

urlpatterns = [
    path('', RecipeListView.as_view(),name='recipelist'),
    path('create/', RecipeCreatView.as_view(),name='recipecreate'),
    path('search/', RecipeSearchView.as_view(),name='recipesearch'),
    path('history/', UserHistoryView.as_view(),name='recipehistory'),
    path('<slug:slug>/', RecipeDetailView.as_view(),name='recipedetail'),
    path('<slug:slug>/update/', RecipeUpdateView.as_view(),name='recipeupdate'),
    path('<slug:slug>/delete/', RecipeCreatView.as_view(),name='recipedelete'),
]
