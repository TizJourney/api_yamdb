from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_superuser or
                request.user.role == User.Role.ADMIN
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение позволяющее только
    superuser и admin редактировать его.
    """

    def has_permission(self, request, view):
        return (
            request.method == 'GET' or
            request.user.is_superuser or
            (
                request.user.is_authenticated and
                request.user.role == User.Role.ADMIN
            )
        )


class IsUserOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user:
            return True
        return (
            request.method == 'DELETE' and
            request.user.role == User.Role.MODERATOR
        )
