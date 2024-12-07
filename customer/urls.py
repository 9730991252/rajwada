from django.urls import path
from . import views
urlpatterns = [
    path('<str:scan_url>', views.customer_scan, name='customer_scan'),
]