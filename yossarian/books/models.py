from django.db import models
from django.contrib.auth.models import User

from yossarian.utils import TimeStampMixin


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

    added_by = models.ForeignKey(User)

    def __str__(self):
        return "<{} - {}>".format(self.id, self.title[:30])

    class Meta:
        ordering = ['average_rating']
