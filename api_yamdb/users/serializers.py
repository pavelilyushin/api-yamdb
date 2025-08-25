"""Сериализаторы для приложения users."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.constants import (
    USERNAME_MAX_LENGTH,
    USER_EMAIL_MAX_LENGTH,
)
from users.validators import (
    validate_username_pattern,
    validate_username_reserved,
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


class UserMeSerializer(UserSerializer):
    """Сериализатор для профиля пользователя."""

    class Meta(UserSerializer.Meta):
        """Мета-класс для UserMeSerializer."""

        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    email = serializers.EmailField(max_length=USER_EMAIL_MAX_LENGTH)

    def validate_username(self, value):
        """Проверка username на запрещенные значения и паттерн."""
        value = validate_username_reserved(value)
        return validate_username_pattern(value)

    def validate(self, data):
        """Проверка уникальности username и email."""
        username = data.get('username')
        email = data.get('email')

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username and user_by_username.email == email:
            return data

        if user_by_email and user_by_email.username != username:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )

        if user_by_username and user_by_username.email != email:
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )

        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        """Проверка существования пользователя и корректности кода."""
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'}
            )

        data['user'] = user
        return data
