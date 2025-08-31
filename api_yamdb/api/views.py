"""Views для API приложения."""

from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlePostMethodSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    UserMeSerializer,
    SignUpSerializer,
    TokenSerializer
)
from reviews.models import Category, Genre, Title, Review, Comment
from .permissions import (
    AdminModerAuthorOrReadOnly,
    IsAdminOrReadOnly,
    IsAdminOrSuperuser
)
from users.utils import generate_confirmation_code, create_or_update_user

User = get_user_model()


class CreateDestroyListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для создания, удаления и списка объектов."""

    pass


class CategoryViewSet(CreateDestroyListViewSet):
    """ViewSet для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    """ViewSet для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title."""

    queryset = Title.objects.annotate(avg_rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'delete', 'patch', 'head', 'options')

    def get_serializer_class(self):
        """Возвращает соответствующий сериализатор в зависимости от метода."""
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostMethodSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""

    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AdminModerAuthorOrReadOnly,)

    def get_queryset(self):
        """Возвращает queryset отзывов для конкретного произведения."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создает отзыв для конкретного произведения."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""

    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AdminModerAuthorOrReadOnly,)

    def get_queryset(self):
        """Возвращает queryset комментариев для конкретного отзыва."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('reviews_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для конкретного отзыва."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('reviews_id'))
        serializer.save(author=self.request.user, review=review)


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
