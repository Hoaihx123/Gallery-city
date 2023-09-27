from django.urls import path
from . import views

urlpatterns = [
    path('setting', views.setting, name='setting'),
]