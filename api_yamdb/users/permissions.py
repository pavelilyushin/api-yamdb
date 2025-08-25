"""Разрешения для приложения users."""

from rest_framework import permissions
# Это все стоит перенести в api

class IsAdminOrSuperuser(permissions.BasePermission):
    """Разрешение для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        """Проверяет, имеет ли пользователь права администратора."""
        return request.user.is_authenticated and request.user.is_admin
