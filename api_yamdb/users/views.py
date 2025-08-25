"""Представления для приложения users."""

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdminOrSuperuser
from users.serializers import (
    UserSerializer, UserMeSerializer,
    SignUpSerializer, TokenSerializer
)
from users.utils import generate_confirmation_code, create_or_update_user

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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SignUpView(APIView):
    """Представление для регистрации пользователя."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Регистрация нового пользователя."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        confirmation_code = generate_confirmation_code()

        create_or_update_user(username, email, confirmation_code)

        send_mail(
            'Код подтверждения для YaMDb',
            f'Ваш код подтверждения: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """Представление для получения JWT токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Получение JWT токена."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
