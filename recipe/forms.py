from django.forms import ModelForm
from .models import Recipe

class RecipeCreateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'servings', 'prep_time', 'instructions']

class RecipeUpdateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'servings', 'prep_time', 'instructions']