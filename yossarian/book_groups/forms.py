from django import forms
from django.forms import ModelForm

from .models import BookGroup


class BookGroupForm(ModelForm):
    name = forms.CharField(max_length=300, required=False)

    class Meta:
        model = BookGroup
        fields = ['name', 'book', 'members']
