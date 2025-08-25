"""Утилиты для приложения users."""

import random
import string

from users.constants import CONFIRMATION_CODE_LENGTH


def generate_confirmation_code():
    """Генерирует код подтверждения."""
    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=CONFIRMATION_CODE_LENGTH
        )
    )


def create_or_update_user(username, email, confirmation_code):
    """Создает нового пользователя или обновляет существующего."""
    from django.contrib.auth import get_user_model
    user_model = get_user_model()

    existing_user = user_model.objects.filter(
        username=username,
        email=email
    ).first()

    if existing_user:
        existing_user.confirmation_code = confirmation_code
        existing_user.save()
        return existing_user

    return user_model.objects.create(
        username=username,
        email=email,
        confirmation_code=confirmation_code
    )
