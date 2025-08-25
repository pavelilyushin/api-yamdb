"""Представления для приложения users."""

import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import AccessToken

from users.constants import CONFIRMATION_CODE_LENGTH
from users.permissions import IsAdminOrSuperuser
from users.serializers import (
    UserSerializer, UserMeSerializer,
    SignUpSerializer, TokenSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperuser,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer
    )
    def me(self, request):
        """Получение и обновление профиля текущего пользователя."""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _generate_confirmation_code(): # Утилиты не должны находиться во вью
    """Генерирует код подтверждения."""
    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=CONFIRMATION_CODE_LENGTH
        )
    )


def _validate_user_uniqueness(username, email): # Подобная проверка должна быть на уровне сериализатора
    """Проверяет уникальность username и email."""
    existing_user_by_username = User.objects.filter(username=username).first()
    existing_user_by_email = User.objects.filter(email=email).first()

    if existing_user_by_email and existing_user_by_email.username != username:
        return False, 'Пользователь с таким email уже существует'

    if existing_user_by_username and existing_user_by_username.email != email:
        return False, 'Пользователь с таким username уже существует'

    return True, existing_user_by_username


def _create_or_update_user(username, email, confirmation_code):
    """Создает нового пользователя или обновляет существующего."""
    existing_user = User.objects.filter(
        username=username,
        email=email
    ).first()

    if existing_user:
        existing_user.confirmation_code = confirmation_code
        existing_user.save()
        return existing_user

    return User.objects.create(
        username=username,
        email=email,
        confirmation_code=confirmation_code
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация нового пользователя."""
    serializer = SignUpSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    is_valid, result = _validate_user_uniqueness(username, email)
    if not is_valid:
        return Response(
            {'error': result},
            status=status.HTTP_400_BAD_REQUEST
        )

    confirmation_code = _generate_confirmation_code()

    _create_or_update_user(username, email, confirmation_code)

    send_mail(
        'Код подтверждения для YaMDb',
        f'Ваш код подтверждения: {confirmation_code}',
        'noreply@yamdb.com', # Адрес - в настройки
        [email]
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получение JWT токена."""
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {'error': 'Пользователь не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    if user.confirmation_code != confirmation_code: # Валидацию стоит унести на уровень сериализатора
        return Response(
            {'error': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )

    token = AccessToken.for_user(user)
    return Response(
        {'token': str(token)},
        status=status.HTTP_200_OK
    )
