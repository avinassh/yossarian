from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import BookGroup, Progress, Comment
from .forms import CommentVoteForm, CreateCommentForm


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


class BookGroupDetailView(DetailView):
    model = BookGroup
    context_object_name = 'book_group'

    def get_context_data(self, object):
        context = super(BookGroupDetailView, self).get_context_data(
            object=object)
        try:
            user = self.request.user
            progress = Progress.objects.get(book_group=object, user=user)
            if progress:
                context['progress'] = progress
        except (TypeError, Progress.DoesNotExist):
            pass
        context['comments'] = Comment.objects.filter(book=object.book)
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


class CommentVoteView(UpdateView):
    model = Comment
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
                    'status': 'success',
                    'comment': {
                        'id': comment.id,
                        'html_comment': comment.html_comment,
                        'author_name': comment.author_name
                    }
                }
        return response
