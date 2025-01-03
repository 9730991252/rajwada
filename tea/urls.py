from django.urls import path
from . import views
urlpatterns = [
path('tea_home/', views.tea_home, name='tea_home'),
path('tea_item/', views.tea_item, name='tea_item'),
path('bill/', views.bill, name='bill'),
path('completed_view_bill/<int:order_filter>', views.completed_view_bill, name='completed_view_bill'),
path('profile/', views.profile, name='profile'),
path('completed_bill/', views.completed_bill, name='completed_bill'),
path('report/', views.report, name='report'),

]