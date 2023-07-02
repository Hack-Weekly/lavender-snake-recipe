from django.db import models
from django.utils.text import slugify

class Recipe(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    recipe_image=models.ImageField(upload_to='recipe_images',default='recipe_images/default_recipe.jpg', blank=True, null=True)
    tags=models.ManyToManyField('Tag', blank=True)
    slug = models.SlugField(max_length=255, unique=True,blank=True,null=True)
    ingredients = models.TextField()
    servings = models.PositiveIntegerField()
    prep_time = models.PositiveIntegerField()
    instructions = models.TextField()



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