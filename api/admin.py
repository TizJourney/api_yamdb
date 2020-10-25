from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model
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
