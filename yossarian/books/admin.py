from django.contrib import admin

from .models import Book, WeeklyBook


class BookAdmin(admin.ModelAdmin):
    list_filter = ('is_reviewed', 'is_contestant')


class WeeklyBookAdmin(admin.ModelAdmin):
    list_filter = ('is_english', 'on_homepage')

admin.site.register(WeeklyBook, WeeklyBookAdmin)
admin.site.register(Book, BookAdmin)
