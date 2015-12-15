from django.db import models
from django.contrib.auth.models import User

from yossarian.utils import TimeStampMixin


class Book(TimeStampMixin):
    goodreads_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    url = models.URLField()

    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    ratings_count = models.IntegerField()

    added_by = models.ForeignKey(User)

    def __str__(self):
        return "<{} - {}>".format(self.id, self.title[:30])

    class Meta:
        ordering = ['average_rating']
