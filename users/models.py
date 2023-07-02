from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio=models.TextField(blank=True,default="")
    def __str__(self):
        return f"{self.username}"

