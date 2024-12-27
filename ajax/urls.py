from django.urls import path
from . import views
urlpatterns = [
    path('participant_list', views.participant_list, name='participant_list'),
    path('save_winner', views.save_winner, name='save_winner'),
    path('add_item_to_cart', views.add_item_to_cart, name='add_item_to_cart'),
    path('cut_item_to_cart', views.cut_item_to_cart, name='cut_item_to_cart'),
    path('search_tea_item', views.search_tea_item, name='search_tea_item'),

]