from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from yossarian.utils import TimeStampMixin

from .validators import is_monday


class Book(TimeStampMixin):
    goodreads_id = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    goodreads_url = models.URLField()
    cover = models.ImageField(upload_to='covers')
    lang_code = models.CharField(max_length=3, default='eng')
    page_count = models.PositiveIntegerField(default=1)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    ratings_count = models.PositiveIntegerField()
    is_reviewed = models.BooleanField(default=False)
    is_contestant = models.BooleanField(default=False)

    added_by = models.ForeignKey(User)

    def __str__(self):
        return "<{} - {}>".format(self.id, self.title[:30])

    class Meta:
        ordering = ['average_rating']


class WeeklyBook(TimeStampMixin):
    week_number = models.PositiveIntegerField(
        unique=True,
        validators=[
            MaxValueValidator(53),
            MinValueValidator(1)
        ])
    week_date = models.DateField(validators=[is_monday])
    is_english = models.BooleanField()
    on_homepage = models.BooleanField(default=False)

    book = models.OneToOneField(Book)

    class Meta:
        unique_together = ('week_number', 'is_english')
        ordering = ['week_number']

    def __str__(self):
        return "<Week {} - {}>".format(self.week_number, self.book.title[:10])


class Vote(TimeStampMixin):

    book = models.ForeignKey(Book)
    value = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(1),
            MinValueValidator(-1)
        ])
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('book', 'user')
