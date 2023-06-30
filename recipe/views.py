from django import http
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

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)



class RecipeUpdateView(UpdateView,LoginRequiredMixin):
    model = Recipe
    template_name = 'recipe/recipe_update.html'
    form_class=RecipeUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise http.Http403("Privilege Error")
        return super().dispatch(request, *args, **kwargs)


class RecipeDeleteView(DeleteView,LoginRequiredMixin):
    model = Recipe
    template_name = 'recipe/recipe_delete.html'
    success_url = '/recipe/'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise http.Http403("Privilege Error")
        return super().dispatch(request, *args, **kwargs)
    