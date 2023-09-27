from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    def __str__(self):
        return self.username
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=64)
    address = models.TextField(max_length=128)
    numphone = models.CharField(max_length=15)
class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=64)
    address = models.TextField(max_length=128)
    birthday = models.TextField(max_length=10)
    bio = models.TextField(max_length=128, blank=True)
    education = models.TextField(max_length=128)
