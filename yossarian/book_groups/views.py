from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import render

from .models import BookGroup, Progress


class BookGroupListView(ListView):
    model = BookGroup
    context_object_name = 'book_groups_list'

    def get_queryset(self):
        try:
            return BookGroup.objects.exclude(members=self.request.user)
        except TypeError:
            return BookGroup.objects.all()


class MyBookGroupListView(ListView):
    model = BookGroup
    context_object_name = 'book_groups_list'

    def get_queryset(self):
        return BookGroup.objects.filter(members=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(MyBookGroupListView, self).get_context_data(**kwargs)
        context['my_groups'] = True
        return context


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

    def get_queryset(self):
        return BookGroup.objects.filter(members=self.request.user)

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
        context['completions'] = Progress.objects.filter(
            is_complete=True).count()
        return render(request, self.template_name, context)


class UpdateProgressView(UpdateView):
    model = Progress
    success_url = '/myprogress/'
    fields = ['pages', 'is_complete']

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)
