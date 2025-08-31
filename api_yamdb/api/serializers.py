"""Сериализаторы для API приложения."""

import datetime as dt

from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment
from reviews.constants import MIN_SCORE, MAX_SCORE
from users.constants import (
    USERNAME_MAX_LENGTH,
    USER_EMAIL_MAX_LENGTH,
)
from users.validators import (
    validate_username_pattern,
    validate_username_reserved,
)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        """Мета-класс для CategorySerializer."""

        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        """Мета-класс для GenreSerializer."""

        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField(source='avg_rating', read_only=True)

    class Meta:
        """Мета-класс для TitleSerializer."""

        model = Title
        fields = (
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre',
            'rating'
        )


class TitlePostMethodSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления Title."""

    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        """Мета-класс для TitlePostMethodSerializer."""

        model = Title
        fields = (
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre',
        )

    def validate_year(self, value):
        """Проверка года выпуска."""
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        """Мета-класс для ReviewSerializer."""

        model = Review
        exclude = ('title',)

    def validate_score(self, value):
        """Проверка оценки на допустимые значения."""
        if not (MIN_SCORE <= value <= MAX_SCORE):
            raise serializers.ValidationError(
                f'Оценивать можно только от {MIN_SCORE} до {MAX_SCORE}! '
                f'{value} не приемлемо!')
        return value

    def validate(self, data):
        """Проверка уникальности отзыва пользователя."""
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and title.reviews.filter(author=author).exists()
        ):
            raise serializers.ValidationError('Ваш отзыв уже засчитан')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Мета-класс для CommentSerializer."""

        model = Comment
        fields = ('id', 'author', 'pub_date', 'text', 'review')


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
