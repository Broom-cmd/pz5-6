from django.contrib import admin
from .models import Movie, Hall, Session, Ticket


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'duration', 'rating')
    search_fields = ('title', 'genre')
    list_filter = ('genre',)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('number', 'hall_type', 'seats_count')
    list_filter = ('hall_type',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'date', 'time', 'price')
    list_filter = ('date', 'hall', 'movie')
    date_hierarchy = 'date'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('session', 'seat_row', 'seat', 'status')
    list_filter = ('status', 'session')