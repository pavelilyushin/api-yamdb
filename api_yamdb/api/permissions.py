from rest_framework import permissions


class AdminModerAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение для администраторов, модераторов и авторов."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_moderator
                or request.user.is_admin
                or obj.author == request.user)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для администраторов или только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminOrSuperuser(permissions.BasePermission):
    """Разрешение только для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        """Проверяет разрешение для запроса."""
        return (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_admin)
        )
