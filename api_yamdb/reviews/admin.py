from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "genre", "name", "year", "description")
    search_fields = ("name",)
    list_filter = ("name", "year", "category", "genre")
    empty_value_display = "-пусто-"


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
