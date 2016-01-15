from django import forms
from django.forms import ModelForm

from .models import CommentVote, Comment


class CommentVoteForm(ModelForm):
    value = forms.IntegerField(min_value=-1, max_value=1)

    class Meta:
        model = CommentVote
        fields = ['value']


class CreateCommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['raw_comment', 'parent', 'book']
