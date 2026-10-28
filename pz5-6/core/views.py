from django.shortcuts import render
from django.utils import timezone
from movies.models import Session


def home(request):
    """Главная — ближайшие сеансы"""
    today = timezone.now().date()
    sessions = (Session.objects
                .filter(date__gte=today)
                .select_related('movie', 'hall')
                .order_by('date', 'time')[:10])
    return render(request, 'core/home.html', {'sessions': sessions})