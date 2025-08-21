from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (
    USER_EMAIL_MAX_LENGTH,
    USER_BIO_MAX_LENGTH,
    USER_ROLE_MAX_LENGTH,
    USER_CONFIRMATION_CODE_MAX_LENGTH
)


class User(AbstractUser):
    """Кастомная модель пользователя с ролями."""

    class Role(models.TextChoices):
        """Роли пользователей в системе."""

        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField(
        'Email',
        max_length=USER_EMAIL_MAX_LENGTH,
        unique=True,
        blank=False
    )
    bio = models.TextField(
        'Биография',
        max_length=USER_BIO_MAX_LENGTH,
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=USER_ROLE_MAX_LENGTH,
        choices=Role.choices,
        default=Role.USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=USER_CONFIRMATION_CODE_MAX_LENGTH,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        """Строковое представление пользователя."""
        return self.username

    @property
    def is_admin(self):
        """Является ли пользователь администратором или суперпользователем."""
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Является ли пользователь модератором."""
        return self.role == self.Role.MODERATOR
