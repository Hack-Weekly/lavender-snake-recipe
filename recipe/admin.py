from django.contrib import admin
from recipe.models import Recipe, Tag,UserHistory,UserFavourite
# Register your models here.
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(UserHistory)
admin.site.register(UserFavourite)