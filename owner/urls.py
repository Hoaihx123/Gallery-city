from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('setting', views.setting, name='setting'),
     path('gallery', views.gallery, name='gallery'),

]