from django.db import models
from django.utils.text import slugify
from django.core.validators import URLValidator


class Recipe(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE,related_name='user_recipes')
    title = models.CharField(max_length=255)
    recipe_image= models.URLField(max_length=1000, default="https://source.unsplash.com/8l8Yl2ruUsg", validators=[URLValidator()])
    tags=models.ManyToManyField('Tag', blank=True)
    slug = models.SlugField(max_length=255, unique=True,blank=True,null=True)
    ingredients = models.TextField()
    servings = models.PositiveIntegerField()
    prep_time = models.PositiveIntegerField()
    instructions = models.TextField()

    def recipe_image_url(self):
        return self.recipe_image

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class UserFavourite(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,related_name='user_favourite')
    recipe = models.ManyToManyField('Recipe',related_name='recipe_favourite')
    def __str__(self):
        return self.user.username + 'favourite' 

class UserHistory(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,related_name='user_history',null=True)
    ip_address= models.GenericIPAddressField(default="0.0.0.0")
    recipe = models.ManyToManyField('Recipe',related_name='recipe_history')
    
    def __str__(self):
        if self.user:
            return self.user.username + 'History' 
        return self.ip_address +' '+'History'