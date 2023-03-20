from rest_framework import permissions


USER_ROLES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.admin

    def has_object_permission(self, request, view, obj):
        return request.user.admin


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
