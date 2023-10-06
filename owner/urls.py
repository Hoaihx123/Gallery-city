from django.urls import path
from . import views

app_name = "owner"  # This is better practice!
urlpatterns = [
    path('', views.manage, name='manage'),
    path('setting', views.setting, name='setting'),
    path('gallery', views.gallery, name='gallery'),
    path('create_exhibit', views.create_exhibit, name='create_exhibit'),
    path('add_artists/<str:exhibit_id>', views.add_artists, name='add_artists'),
    path('info', views.info, name='info')
]
