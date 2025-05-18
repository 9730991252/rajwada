from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]