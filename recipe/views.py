from django import http
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from recipe.forms import RecipeCreateForm, RecipeUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from recipe.models import Recipe,Tag

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_list.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    


class RecipeCreatView(LoginRequiredMixin,CreateView):
    model = Recipe
    template_name = 'recipe/recipe_create.html'
    form_class=RecipeCreateForm

    def form_valid(self,form):
        recipe=form.save(commit=False)
        recipe.author=self.request.user
        recipe.save()
        custom_tags = form.cleaned_data['custom_tags']
        if custom_tags:
            custom_tags = custom_tags.split(' ')
            for custom_tag in custom_tags:
                tag, created = Tag.objects.get_or_create(name=custom_tag.strip())
                recipe.tags.add(tag)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('recipe:recipedetail',kwargs={'slug':self.object.slug})



class RecipeUpdateView(LoginRequiredMixin,UpdateView):
    model = Recipe
    template_name = 'recipe/recipe_update.html'
    form_class=RecipeUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise http.Http403("Privilege Error")
        return super().dispatch(request, *args, **kwargs)


class RecipeDeleteView(LoginRequiredMixin,DeleteView):
    model = Recipe
    template_name = 'recipe/recipe_delete.html'
    success_url = '/recipe/'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise http.Http403("Privilege Error")
        return super().dispatch(request, *args, **kwargs)
    