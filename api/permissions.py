from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser or
            request.user.role == User.Role.ADMIN
        )
