from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage, name='manage'),
    path('setting', views.setting, name='setting'),
    path('add_work', views.add_work, name='add_work'),

]