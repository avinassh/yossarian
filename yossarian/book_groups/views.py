from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, render

from yossarian.books.models import Book

from .models import BookGroup, Progress
from .forms import BookGroupForm


class BookGroupListView(ListView):
    model = BookGroup
    context_object_name = 'book_groups_list'


class MyBookGroupListView(ListView):
    model = BookGroup
    context_object_name = 'book_groups_list'

    def get_queryset(self):
        return BookGroup.objects.filter(members=self.request.user)


class BookGroupCreateView(CreateView):
    model = BookGroup
    form_class = BookGroupForm
    success_url = '/groups/'

    def get_context_data(self, **kwargs):
        try:
            book_id = int(self.request.GET['book'])
            book = get_object_or_404(Book, pk=book_id)
        except (TypeError, ValueError, KeyError):
            raise Http404('Book does not exist')
        context = super(BookGroupCreateView, self).get_context_data(**kwargs)
        context['form'] = BookGroupForm(initial={'book': book_id, 'name': ''})
        context['book'] = book
        return context

    def form_valid(self, form):
        book_group = form.save(commit=False)
        book_group.name = self._get_group_name(form)
        book_group.owner = self.request.user
        book_group.save()
        book_group.members.add(self.request.user)
        Progress.objects.create(book_group=book_group, user=self.request.user)
        return super(BookGroupCreateView, self).form_valid(form)

    def _get_group_name(self, form):
        default_name = form.cleaned_data['book'].title + ' Group'
        group_name = form.cleaned_data.get('name').strip()
        if not group_name:
            return default_name
        return group_name


class BookGroupUpdateView(UpdateView):
    model = BookGroup
    fields = ['name']


class JoinBookGroupView(UpdateView):
    model = BookGroup

    def get(self, request, pk):
        user = self.request.user
        book_group = self.get_object()
        book_group.members.add(user)
        Progress.objects.get_or_create(book_group=book_group, user=user)
        return HttpResponse('You have successfully joined the group')


class LeaveBookGroupView(UpdateView):
    model = BookGroup

    def get(self, request, pk):
        user = self.request.user
        book_group = self.get_object()
        book_group.members.remove(user)
        Progress.objects.filter(book_group=book_group, user=user).delete()
        return HttpResponse('You have successfully left the group')


class MyProgessListView(ListView):
    model = Progress
    context_object_name = 'progress_list'

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)


class BookGroupsProgressView(View):
    template_name = 'book_groups/progress.html'

    def get(self, request):
        context = {}
        context['total'] = BookGroup.objects.count()
        context['users'] = User.objects.exclude(book_groups=None).count()
        context['bg_owners'] = User.objects.exclude(
            owned_book_groups=None).count()
        context['completions'] = Progress.objects.filter(
            is_complete=True).count()
        return render(request, self.template_name, context)


class UpdateProgressView(UpdateView):
    model = Progress
    success_url = '/myprogress/'
    fields = ['pages', 'is_complete']

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)
