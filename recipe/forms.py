from django import forms
from .models import Recipe

class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'servings', 'prep_time', 'instructions']
        widgets = {
            'ingredients': forms.Textarea(attrs={'class': 'h-32 w-96', 'placeholder': 'List ingredients here...'}),
        }

class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'servings', 'prep_time', 'instructions'] 

