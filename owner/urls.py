from django.urls import path
from . import views
urlpatterns = [
    path('owner_home/', views.owner_home, name='owner_home'),
    path('profile/', views.profile, name='profile'),
    path('lucky_draw/', views.lucky_draw, name='lucky_draw'),
    path('winner/', views.winner, name='winner'),
    path('customer/', views.customer, name='customer'),
    path('category/', views.category, name='category'),
    path('item/', views.item, name='item'),
    path('waiter/', views.waiter, name='waiter'),
    path('chef/', views.chef, name='chef'),
    path('table/', views.table, name='table'),
    path('menu_qrcode/', views.menu_qrcode, name='menu_qrcode'),
    path('running_table/', views.running_table, name='running_table'),
    path('view_order/<int:table_id>', views.view_order, name='view_order'),
    path('tea_employee/', views.tea_employee, name='tea_employee'),
    path('complate_order/', views.complate_order, name='complate_order'),
    path('complate_view_order/<int:order_filter>', views.complate_view_order, name='complate_view_order'),
    path('item_detail/<int:id>', views.item_detail, name='item_detail'),
]