from django.db import models
from django.contrib.auth.models import User

from yossarian.utils import TimeStampMixin
from yossarian.books.models import Book


class BookGroup(TimeStampMixin):
    name = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)

    book = models.ForeignKey(Book)
    owner = models.ForeignKey(User, related_name='owned_book_groups')
    members = models.ManyToManyField(User, related_name='book_groups')


class Progress(TimeStampMixin):
    is_complete = models.BooleanField(default=False)
    pages = models.PositiveIntegerField(default=1)

    book_group = models.ForeignKey(BookGroup)
    user = models.ForeignKey(User)