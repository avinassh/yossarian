from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView


from .models import BookGroup


class BookGroupListView(ListView):
    model = BookGroup
    context_object_name = 'book_groups_list'
