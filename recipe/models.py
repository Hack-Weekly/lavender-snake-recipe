from django.db import models
from django.utils.text import slugify

class Recipe(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    servings = models.PositiveIntegerField()
    prep_time = models.PositiveIntegerField()
    instructions = models.TextField()


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

