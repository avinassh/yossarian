from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import BookGroup
from .forms import BookGroupForm


class BookGroupListView(ListView):
    model = BookGroup
    context_object_name = 'book_groups_list'


class BookGroupCreateView(CreateView):
    model = BookGroup
    form_class = BookGroupForm
    success_url = '/groups/'

    def form_valid(self, form):
        book_group = form.save(commit=False)
        book_group.owner = self.request.user
        book_group.save()
        book_group.members.add(self.request.user)
        return super(BookGroupCreateView, self).form_valid(form)
