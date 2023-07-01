from django import forms
from recipe.models import Recipe
from recipe.models import Tag

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class RecipeCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    custom_tags = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Recipe
        fields = ['title','recipe_image','tags','custom_tags', 'ingredients', 'servings', 'prep_time', 'instructions']
        widgets = {
            'ingredients': forms.Textarea(attrs={'class': 'h-32 w-96', 'placeholder': 'List ingredients here...'}),
            'instructions':SummernoteWidget(),
        }

class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title','recipe_image', 'ingredients', 'servings', 'prep_time', 'instructions']
        widgets = {
            'ingredients': forms.Textarea(attrs={'class': 'h-32 w-96', 'placeholder': 'List ingredients here...'}),
            'instructions':SummernoteWidget(),
        } 

