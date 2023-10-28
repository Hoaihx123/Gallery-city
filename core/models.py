from django.db import models
from django.contrib.auth.models import AbstractUser
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files import File
from datetime import datetime
# Create your models here.


execution_choice = (('paint', 'paint'), ('watercolor',
                    'watercolor'), ('sculpture', 'sculpture'))
exhibit_choice = (('fine', 'fine'), ('applied', 'applied'),
                  ('sculpture', 'sculpture'))


class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Owner(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=64)
    address = models.TextField(max_length=128)
    numphone = models.CharField(max_length=15)
    img = models.ImageField(
        upload_to='owners', default='default/default.png', blank=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=64)
    address = models.TextField(max_length=128)
    birthday = models.TextField(max_length=10)
    bio = models.TextField(max_length=128, blank=True)
    education = models.TextField(max_length=128)
    img = models.ImageField(
        upload_to='artists', default='default/default.png', blank=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    owner = models.OneToOneField(
        Owner, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=128)
    acreage = models.IntegerField()
    address = models.TextField(max_length=128)
    img = models.ImageField(upload_to='galleries', blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name


class Exhibit(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    start_time = models.TextField(max_length=10)
    end_time = models.TextField(max_length=10)
    type = models.CharField(choices=execution_choice)
    num_of_tickets = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)
    price = models.IntegerField()
    img = models.ImageField(upload_to='exhibits', blank=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    is_invitation = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

class Work(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    execution = models.CharField(choices=execution_choice)
    data = models.DateField(auto_now_add=True)
    height = models.IntegerField()
    width = models.IntegerField()
    volume = models.IntegerField(blank=True, null=True)
    img = models.ImageField(upload_to='works', blank=True)

    def __str__(self):
        return self.name

class Place(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE)

class Work_Exhibit(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE)
    def __str__(self):
        return self.work.name+self.exhibit.name

class Cart(models.Model):
    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ImageField(blank=True, upload_to='QR-code')
    time = models.TimeField(default=datetime.now)
    def save(self, *args, **kwargs):
        qr_img = qrcode.make(self.id)
        qr_offset = Image.new('RGB', (300, 300), 'white')
        qr_offset.paste(qr_img)
        files_name = f'{self.exhibit.name}-{self.user}gr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)