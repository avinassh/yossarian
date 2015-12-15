from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseBadRequest

from .models import Book
from .forms import BookForm
from .goodreads_api import get_book_details_by_id


class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    success_url = '/'

    def form_valid(self, form):
        book = form.save(commit=False)
        book.added_by = self.request.user
        book_details = get_book_details_by_id(book.goodreads_id)

        if not book_details:
            return HttpResponseBadRequest('piss be entering valid id')

        book.title = book_details.get('title')
        book.average_rating = book_details.get('average_rating')
        book.ratings_count = book_details.get('ratings_count')
        book.description = book_details.get('description')
        book.url = book_details.get('url')

        return super(BookCreateView, self).form_valid(form)
