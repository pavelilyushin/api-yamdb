"""Валидаторы для приложения users."""

import re

from rest_framework import serializers

from users.constants import USERNAME_PATTERN


def validate_username_pattern(value):
    """Проверяет соответствие username паттерну."""
    if not re.match(USERNAME_PATTERN, value):
        raise serializers.ValidationError(
            'Username должен соответствовать паттерну: ^[\\w.@+-]+\\Z'
        )
    return value


def validate_username_reserved(value):
    """Проверяет, что username не является зарезервированным."""
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Использовать имя "me" в качестве username запрещено.'
        )
    return value
