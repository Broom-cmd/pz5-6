from django.db import models

from django.db import models


class Movie(models.Model):
    """Фильм"""
    title = models.CharField('Название', max_length=200)
    genre = models.CharField('Жанр', max_length=100)
    duration = models.PositiveIntegerField('Длительность, мин')
    rating = models.DecimalField(
        'Рейтинг', max_digits=3, decimal_places=1,
        null=True, blank=True
    )
    description = models.TextField('Описание', blank=True, default='')

    class Meta:
        db_table = 'movie'          # имя таблицы в БД
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Hall(models.Model):
    """Зал"""
    HALL_TYPES = [
        ('2D', '2D'),
        ('3D', '3D'),
        ('IMAX', 'IMAX'),
    ]
    number = models.PositiveIntegerField('Номер зала', unique=True)
    seats_count = models.PositiveIntegerField('Количество мест')
    hall_type = models.CharField('Тип', max_length=10, choices=HALL_TYPES)

    class Meta:
        db_table = 'hall'
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'
        ordering = ['number']

    def __str__(self):
        return f'Зал №{self.number} ({self.hall_type})'


class Session(models.Model):
    """Сеанс"""
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name='Фильм'
    )
    hall = models.ForeignKey(
        Hall,
        on_delete=models.PROTECT,
        related_name='sessions',
        verbose_name='Зал'
    )
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    price = models.DecimalField('Цена, ₽', max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'session'
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'
        ordering = ['date', 'time']
        unique_together = [('hall', 'date', 'time')]

    def __str__(self):
        return f'{self.movie.title} — {self.date} {self.time:%H:%M}'


class Ticket(models.Model):
    """Билет"""
    STATUS_CHOICES = [
        ('продан', 'Продан'),
        ('свободен', 'Свободен'),
    ]
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='Сеанс'
    )
    seat_row = models.PositiveIntegerField('Ряд')
    seat = models.PositiveIntegerField('Место')
    status = models.CharField(
        'Статус', max_length=10,
        choices=STATUS_CHOICES, default='свободен'
    )

    class Meta:
        db_table = 'ticket'
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        unique_together = [('session', 'seat_row', 'seat')]

    def __str__(self):
        return f'Ряд {self.seat_row}, место {self.seat} ({self.status})'