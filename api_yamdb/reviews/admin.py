from django.contrib import admin
from .models import User, Category, Genre, Title, Review, Comment


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


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "text", "score", "pub_date")
    search_fields = ("title",)
    list_filter = ("title", "author", "score", "pub_date")
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "review", "text", "pub_date")
    search_fields = ("author",)
    list_filter = ("author", "text", "pub_date")
    empty_value_display = "-пусто-"


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
