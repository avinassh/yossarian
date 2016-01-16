import tempfile
import random

import requests
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.http import HttpResponseBadRequest, JsonResponse
from django.template.defaulttags import register
from django.core.files import File
from django.utils import timezone

from yossarian.book_groups.models import BookGroup

from .models import Book, Vote, Comment
from .forms import BookForm, ArenaVoteForm, CommentVoteForm, CreateCommentForm
from .goodreads_api import get_book_details_by_id


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


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
        image_url = book_details.get('image_url')
        save_book_cover(book, img_name=book.goodreads_id, img_url=image_url)
        BookGroup.objects.create(book=book, name=book.title)
        return super(BookCreateView, self).form_valid(form)


class ArenaView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/arena.html'

    def get_queryset(self):
        return Book.objects.filter(is_reviewed=True, is_contestant=True)

    def get_context_data(self, **kwargs):
        query_set = self.get_queryset()
        count = query_set.count()
        if count > 20:
            random_ids = random.sample(range(1, count), 20)
            self.query_set = query_set.filter(id__in=random_ids)
        if self.request.user.is_authenticated():
            context = super(ArenaView, self).get_context_data(**kwargs)
            user = self.request.user
            votes_list = {}
            for book in context['book_list']:
                try:
                    vote = Vote.objects.get(book=book, user=user)
                    votes_list[book.id] = vote.value
                except Vote.DoesNotExist:
                    votes_list[book.id] = 0
            context['votes_list'] = votes_list
            return context
        return super(ArenaView, self).get_context_data(**kwargs)


class UpdateArenaVoteView(UpdateView):
    model = Book
    form_class = ArenaVoteForm

    def form_valid(self, form):
        vote_value = form.cleaned_data['value']
        book = self.object
        user = self.request.user
        vote, created = Vote.objects.update_or_create(
            book=book, user=user, defaults={'value': vote_value})
        if vote:
            return JsonResponse({"voteValue": vote_value})


def save_book_cover(book, img_name, img_url):
    if not img_url:
        return
    r = requests.get(img_url, stream=True)
    with tempfile.NamedTemporaryFile() as fp:
        for block in r.iter_content(1024 * 8):
            if not block:
                break
            fp.write(block)
        book.cover.save(str(img_name) + '.jpg', File(fp))
    return True


class HomePageView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_list.html'

    def get_queryset(self):
        today = timezone.now()
        current_week_number = today.isocalendar()[1]
        return Book.objects.filter(weeklybook__week_number=current_week_number)


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, object):
        context = super(BookDetailView, self).get_context_data(
            object=object)
        context['comments'] = Comment.objects.filter(book=object)
        return context


class CommentVoteView(UpdateView):
    form_class = CommentVoteForm


class CommentCreateView(View):
    form_class = CreateCommentForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.html_comment = comment.raw_comment
            comment.author = self.request.user
            comment.author_name = self.request.user.username
            comment.save()
            response = self.get_response_dict(comment)
            return JsonResponse(response)

    def get_response_dict(self, comment):
        response = {
                    'success': True,
                    'comment': {
                        'id': comment.id,
                        'html_comment': comment.html_comment,
                        'author_name': comment.author_name
                    }
                }
        return response
