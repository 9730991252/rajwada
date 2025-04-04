from django.urls import path
from . import views
urlpatterns = [
    path('participant_list', views.participant_list, name='participant_list'),
    path('save_winner', views.save_winner, name='save_winner'),
    path('add_item_to_cart', views.add_item_to_cart, name='add_item_to_cart'),
    path('cut_item_to_cart', views.cut_item_to_cart, name='cut_item_to_cart'),
    path('search_tea_item', views.search_tea_item, name='search_tea_item'),
    path('add_item_to_hotel_cart', views.add_item_to_hotel_cart, name='add_item_to_hotel_cart'),
    path('search_hotel_item', views.search_hotel_item, name='search_hotel_item'),
    path('filter_items_by_category', views.filter_items_by_category, name='filter_items_by_category'),
    path('select_category_item', views.select_category_item, name='select_category_item'),
    path('search_tea_item_by_category', views.search_tea_item_by_category, name='search_tea_item_by_category'),
    path('select_discount_percent', views.select_discount_percent, name='select_discount_percent'),
    path('select_item_category/', views.select_item_category, name='select_item_category'),
    path('chang_teble_status/', views.chang_teble_status, name='chang_teble_status'),
    path('chang_teble_name/', views.chang_teble_name, name='chang_teble_name'),
    path('add_item_to_cart_edit/', views.add_item_to_cart_edit, name='add_item_to_cart_edit'),
    
    ]