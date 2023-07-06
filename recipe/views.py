from django import http
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from recipe.forms import RecipeCreateForm, RecipeUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from recipe.models import Recipe,Tag
from recipe.features import get_similar_recipes_by_tags, search_recipes
from recipe.features import create_or_add_to_history
from ipware import get_client_ip
from recipe.models import UserFavourite,UserHistory

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'recipe'

    def dispatch(self, request, *args, **kwargs):
        recipe = self.get_object()
        create_or_add_to_history(request, recipe)
        return super().dispatch(request, *args, **kwargs)
    

class RecipeSearchView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_search.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return search_recipes(query)
        return Recipe.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query')
        return context


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
            raise PermissionDenied("Privilege Error")
            #code for 403 error
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('recipe:recipedetail',kwargs={'slug':self.object.slug})


class RecipeDeleteView(LoginRequiredMixin,DeleteView):
    model = Recipe
    template_name = 'recipe/recipe_delete.html'
    success_url = '/recipe/'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise PermissionDenied("Privilege Error")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('recipe:recipelist')
    
class UserHistoryView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_history.html'
    context_object_name = 'recipes'

    def get_queryset(self):

        try:
            if self.request.user.is_authenticated:
                return UserHistory.objects.get(user=self.request.user).recipe.all()
            else:
                client_ip, is_routable = get_client_ip(self.request)
                return UserHistory.objects.get(ip_address=client_ip).recipe.all()
        except Exception as e:
            return Recipe.objects.none()
    

