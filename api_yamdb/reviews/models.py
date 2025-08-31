import datetime as dt
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from .constants import (
    MAX_LENGTH,
    MAX_SCORE,
    MIN_SCORE,
    MIN_YEAR,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
)

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
        max_length=SLUG_MAX_LENGTH
    )

    def __str__(self):
        return self.name[:MAX_LENGTH]

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        max_length=SLUG_MAX_LENGTH
    )

    def __str__(self):
        return self.name[:MAX_LENGTH]

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Наименование'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(MIN_YEAR, message='Год не может быть меньше 1'),
            MaxValueValidator(
                dt.date.today().year,
                message='Год не может быть больше текущего'
            )
        ]
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр',
    )

    class Meta:
        default_related_name = 'titles'
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:MAX_LENGTH]


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ]
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['title', 'author'],
                                               name='unique_review')]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации коммента',
        auto_now_add=True
    )
    text = models.TextField(verbose_name='Текст комментария')
