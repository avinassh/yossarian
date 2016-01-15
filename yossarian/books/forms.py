from django import forms
from django.forms import ModelForm

from .models import Book, Vote


class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['goodreads_id']


class ArenaVoteForm(ModelForm):
    value = forms.IntegerField(min_value=0, max_value=1)

    class Meta:
        model = Vote
        fields = ['value']
