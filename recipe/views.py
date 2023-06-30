from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from recipe.forms import RecipeCreateForm, RecipeUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from recipe.models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_list.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'

class RecipeCreatView(CreateView,LoginRequiredMixin):
    model = Recipe
    template_name = 'recipe/recipe_create.html'
    form_class=RecipeCreateForm


class RecipeUpdateView(UpdateView,LoginRequiredMixin):
    model = Recipe
    template_name = 'recipe/recipe_update.html'
    form_class=RecipeUpdateForm

class RecipeDeleteView(DeleteView,LoginRequiredMixin):
    model = Recipe
    template_name = 'recipe/recipe_delete.html'
    success_url = '/recipe/'