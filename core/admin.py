from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Owner)
admin.site.register(models.Artist)
admin.site.register(models.Gallery)
admin.site.register(models.Work)


