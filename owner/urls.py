from django.urls import path
from . import views

urlpatterns = [
     path('', views.manage, name='manage'),
     path('setting', views.setting, name='setting'),
     path('gallery', views.gallery, name='gallery'),
     path('create_exhibit', views.create_exhibit, name='create_exhibit')

]