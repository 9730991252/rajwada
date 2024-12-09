from django.urls import path
from . import views
urlpatterns = [
    path('participant_list', views.participant_list, name='participant_list'),
    path('save_winner', views.save_winner, name='save_winner'),

]