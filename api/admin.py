from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Comment, Review


User = get_user_model()


class YamDBUserAdmin(UserAdmin):
    model = User
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name',  'bio', 'role'),
        }),
    )
    fieldsets = UserAdmin.fieldsets +  (
        (None, {
            'classes': ('wide',),
            'fields': ('bio', 'role'),
        }),
    )
    list_display = ('username', 'email', 'bio', 'role')

admin.site.register(User, YamDBUserAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('author',)
    list_filter = ('pub_date',)


admin.site.register(Comment, CommentAdmin)
