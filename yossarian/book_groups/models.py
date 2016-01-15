from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey

from yossarian.utils import TimeStampMixin


class BookGroup(TimeStampMixin):
    name = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)

    book = models.OneToOneField('books.Book')
    members = models.ManyToManyField(User, related_name='book_groups')


class Progress(TimeStampMixin):
    is_complete = models.BooleanField(default=False)
    pages = models.PositiveIntegerField(default=1)

    book_group = models.ForeignKey(BookGroup)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('book_group', 'user')


class Comment(MPTTModel, TimeStampMixin):
    author_name = models.CharField(null=False, max_length=12)
    raw_comment = models.TextField()
    html_comment = models.TextField()
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    author = models.ForeignKey(User)
    parent = TreeForeignKey('self', related_name='children',
                            null=True, blank=True, db_index=True)
    book = models.ForeignKey('books.Book')

    class MPTTMeta:
        order_insertion_by = ['-score']


class CommentVote(TimeStampMixin):
    value = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(1),
            MinValueValidator(-1)
        ])

    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('comment', 'user')
