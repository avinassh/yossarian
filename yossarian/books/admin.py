from django.contrib import admin

from .models import Book, WeeklyBook

admin.site.register(Book)
admin.site.register(WeeklyBook)
