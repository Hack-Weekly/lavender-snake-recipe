from django.contrib import admin
from recipe.models import Recipe, Tag
# Register your models here.
admin.site.register(Recipe)
admin.site.register(Tag)