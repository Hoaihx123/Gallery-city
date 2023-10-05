from django.urls import path
from . import views

app_name = "artist"  # This is better practice!
urlpatterns = [
    path('', views.manage, name='manage'),
    path('setting', views.setting, name='setting'),
    path('add_work', views.add_work, name='add_work'),
    path('work_manage', views.work_manage, name='work_manage'),

]
