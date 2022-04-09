from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='user_images', blank=True)
    age = models.PositiveIntegerField(default=18)
    email = models.EmailField(unique=True, blank=False)
