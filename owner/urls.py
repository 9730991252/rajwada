from django.urls import path
from . import views
urlpatterns = [
    path('owner_home/', views.owner_home, name='owner_home'),
    path('profile/', views.profile, name='profile'),
    path('add_bill/', views.add_bill, name='add_bill'),
    path('lucky_draw/', views.lucky_draw, name='lucky_draw'),
    path('winner/', views.winner, name='winner'),
    path('customer/', views.customer, name='customer'),
    path('view_bill/<int:id>', views.view_bill, name='view_bill'),
]