from django.urls import path
from . import views

urlpatterns = [
path('chef_home/', views.chef_home, name='chef_home')
]
