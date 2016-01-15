from django import forms
from django.forms import ModelForm

from .models import CommentVote


class CommentVoteForm(ModelForm):
    value = forms.IntegerField(min_value=-1, max_value=1)

    class Meta:
        model = CommentVote
        fields = ['value']
