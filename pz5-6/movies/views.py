from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Movie, Session, Ticket


def movie_list(request):
    """Список всех фильмов. Поддерживает фильтр ?genre=..."""
    genre = request.GET.get('genre')
    movies = Movie.objects.all()
    if genre:
        movies = movies.filter(genre__icontains=genre)
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genre': genre,
    })


def movie_detail(request, pk):
    """Карточка фильма + его сеансы"""
    movie = get_object_or_404(Movie, pk=pk)
    sessions = movie.sessions.select_related('hall').order_by('date', 'time')
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'sessions': sessions,
    })


def session_list(request):
    """Сеансы на дату (?date=YYYY-MM-DD) или все будущие"""
    date_str = request.GET.get('date')
    sessions = Session.objects.select_related('movie', 'hall')
    if date_str:
        sessions = sessions.filter(date=date_str)
    else:
        sessions = sessions.filter(date__gte=timezone.now().date())
    sessions = sessions.order_by('date', 'time')
    return render(request, 'movies/session_list.html', {
        'sessions': sessions,
        'date': date_str,
    })


def ticket_create(request):
    """Покупка билета"""
    if request.method == 'POST':
        session_id = request.POST.get('session')
        seat_row = request.POST.get('seat_row')
        seat = request.POST.get('seat')
        session = get_object_or_404(Session, pk=session_id)
        ticket, created = Ticket.objects.get_or_create(
            session=session, seat_row=seat_row, seat=seat,
            defaults={'status': 'продан'}
        )
        if not created:
            ticket.status = 'продан'
            ticket.save()
        return redirect('movies:movie_detail', pk=session.movie.pk)

    # GET — показываем форму
    sessions = Session.objects.select_related('movie', 'hall')
    return render(request, 'movies/ticket_form.html', {'sessions': sessions})