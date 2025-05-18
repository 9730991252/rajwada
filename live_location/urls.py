from .views import *
from django.urls import path

urlpatterns = [
    path('',lindex,name='index'),
    path('send_location/',send_location,name='send_location'),
    path('produce_lat_lon/',produce_lat_lon,name='produce_lat_lon'),
    path('data/',data,name='data'),
]