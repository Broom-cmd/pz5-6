from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('sessions/', views.session_list, name='session_list'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),
]