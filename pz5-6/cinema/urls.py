from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),       # главная
    path('', include('movies.urls')),     # фильмы, сеансы, билеты
]