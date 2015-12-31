from django.forms import ModelForm

from .models import BookGroup


class BookGroupForm(ModelForm):

    class Meta:
        model = BookGroup
        fields = ['name', 'book', 'members']
