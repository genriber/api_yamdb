from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == "admin"


class AdminOnly(permissions.BasePermission):
    """Премишен админа или суперпользователя"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "admin" or request.user.is_superuser


class IsAdOrModOrAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(
                request.user.role == "moderator"
                or request.user.role == "admin"
                or obj.author == request.user
            )
