from django.db import models


# Добавил получение модели пользователя
from django.contrib.auth import get_user_model
User = get_user_model()


MAX_LENGTH = 25


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')

    def __str__(self):
        return self.name[:MAX_LENGTH]

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(verbose_name='Слаг жанра')

    def __str__(self):
        return self.name[:MAX_LENGTH]

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Наименование')
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    year = models.IntegerField(verbose_name='Год выпуска')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр',
    )

    def __str__(self):
        return self.name[:MAX_LENGTH]

    class Meta:
        default_related_name = 'titles'
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    rewiew_title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    rewiew_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    rewiew_pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True
    )
    review_text = models.TextField()


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )
    comment_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    comment_pub_date = models.DateTimeField(
        verbose_name='Дата публикации коммента',
        auto_now_add=True
    )
    comment_text = models.TextField()
