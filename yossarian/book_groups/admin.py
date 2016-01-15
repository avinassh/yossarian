from django.contrib import admin

from .models import BookGroup, Progress, Comment

admin.site.register(BookGroup)
admin.site.register(Progress)
admin.site.register(Comment)
