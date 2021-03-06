"""yossarian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from yossarian.books.views import (
    BookCreateView, BookListView, ArenaView, UpdateArenaVoteView,
    HomePageView, BookDetailView, CommentCreateView)
from yossarian.book_groups.views import (
    BookGroupListView, JoinBookGroupView,
    LeaveBookGroupView, MyBookGroupListView, MyProgessListView,
    BookGroupsProgressView, UpdateProgressView, BookGroupDetailView)

urlpatterns = [
    url(r'^$', HomePageView.as_view()),
    url(r'^books/(?P<pk>[0-9]+)/$', BookDetailView.as_view(),
        name='books-detail'),
    url(r'^books/$', BookListView.as_view()),
    url(r'^arena/$', ArenaView.as_view()),
    url(r'^arena_vote/(?P<pk>[0-9]+)/$', UpdateArenaVoteView.as_view()),
    url(r'^mygroups/$', MyBookGroupListView.as_view()),
    url(r'^myprogress/$', MyProgessListView.as_view()),
    url(r'^updateprogress/(?P<pk>[0-9]+)/$', UpdateProgressView.as_view()),
    url(r'^progress/$', BookGroupsProgressView.as_view()),
    url(r'^join/(?P<pk>[0-9]+)/$', JoinBookGroupView.as_view(), name='join'),
    url(r'^leave/(?P<pk>[0-9]+)/$', LeaveBookGroupView.as_view(),
        name='leave'),
    url(r'^groups/(?P<pk>[0-9]+)/$', BookGroupDetailView.as_view(),
        name='groups-detail'),
    url(r'^groups/', BookGroupListView.as_view()),
    url(r'^comments/$', CommentCreateView.as_view()),
    url(r'^add/', BookCreateView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += patterns(
        '', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
