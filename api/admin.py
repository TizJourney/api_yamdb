from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class YamDBUserAdmin(UserAdmin):
    model = User
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'first_name',
                'last_name',
                'bio', 'role'),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('bio', 'role'),
        }),
    )
    list_display = ('username', 'email', 'bio', 'role')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('author',)
    list_filter = ('pub_date',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'join_genres', 'category')
    search_fields = ('name', 'year', 'genre', 'category')
    list_filter = ('year', 'genre', 'category')

    def join_genres(self, obj):
        return ', '.join([str(g) for g in obj.genre.all()])


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


admin.site.register(User, YamDBUserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
