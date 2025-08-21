"""Сериализаторы для приложения users."""

import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.constants import (
    USERNAME_PATTERN,
    USERNAME_MAX_LENGTH,
    USER_EMAIL_MAX_LENGTH,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        """Мета-класс для UserSerializer."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя."""

    class Meta:
        """Мета-класс для UserMeSerializer."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


def _validate_username_pattern(value):
    """Проверяет соответствие username паттерну."""
    if not re.match(USERNAME_PATTERN, value):
        raise serializers.ValidationError(
            'Username должен соответствовать паттерну: ^[\\w.@+-]+\\Z'
        )
    return value


def _validate_username_reserved(value):
    """Проверяет, что username не является зарезервированным."""
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Использовать имя "me" в качестве username запрещено.'
        )
    return value


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    email = serializers.EmailField(max_length=USER_EMAIL_MAX_LENGTH)

    def validate_username(self, value):
        """Проверка username на запрещенные значения и паттерн."""
        value = _validate_username_reserved(value)
        return _validate_username_pattern(value)


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
