"""Константы для приложения users."""

# Константы для пользователей
USER_EMAIL_MAX_LENGTH = 254
USER_BIO_MAX_LENGTH = 500
USER_ROLE_MAX_LENGTH = 20
USER_CONFIRMATION_CODE_MAX_LENGTH = 100

# Длина кода подтверждения
CONFIRMATION_CODE_LENGTH = 6

# Регулярное выражение для валидации username
USERNAME_PATTERN = r'^[\w.@+-]+\Z'

# Дополнительные константы для сериализаторов
# Максимальная длина username
USERNAME_MAX_LENGTH = 150
