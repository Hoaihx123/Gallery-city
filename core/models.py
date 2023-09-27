from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


execution_choice = (('paint', 'paint'), ('watercolor', 'watercolor'), ('sculpture', 'sculpture'))

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
    def __str__(self):
        return self.name
class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=64)
    address = models.TextField(max_length=128)
    birthday = models.TextField(max_length=10)
    bio = models.TextField(max_length=128, blank=True)
    education = models.TextField(max_length=128)
    def __str__(self):
        return self.name
class Gallery(models.Model):
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=128)
    acreage = models.IntegerField()
    address = models.TextField(max_length=128)
    def __str__(self):
        return self.name

class Work(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    execution = models.CharField(choices=execution_choice)
    data = models.DateField(auto_now_add=True)
    height = models.IntegerField()
    width = models.IntegerField()
    volume = models.IntegerField(blank=True)
    def __str__(self):
        return self.name
