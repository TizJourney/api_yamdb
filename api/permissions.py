from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Только superuser и admin разрешено использовать небезопасные методы.
    """

    def has_permission(self, request, view):
        return (
            request.method == 'GET' or
            (request.user.is_authenticated and request.user.is_admin)
        )


class IsUserOrModerator(permissions.BasePermission):
    """
    Только автору и модератору разрешено использовать небезопасные методы.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.author == request.user or
            (request.method == 'DELETE' and request.user.is_moderator)
        )
