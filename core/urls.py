from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('exhibit/<str:exhibit_id>', views.exhibit_view, name='exhibit_view'),
    path('gallery/<str:owner_id>', views.gallery_view, name='gallery_view'),
    path('buy_ticket', views.buy_ticket, name='buy_ticket'),

]
