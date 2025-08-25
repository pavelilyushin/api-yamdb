from django.db import models
# Валидаторы для оценки от 1 до 10
from django.core.validators import MaxValueValidator, MinValueValidator


# Добавил получение модели пользователя
from django.contrib.auth import get_user_model
User = get_user_model()


MAX_LENGTH = 25


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
        max_length=50
    )

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
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        max_length=50
    )

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
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр',
    )

    def __str__(self):
        return self.name[:MAX_LENGTH]

    @property
    def rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return None
        return sum(review.score for review in reviews) / len(reviews)

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
            MaxValueValidator(10),
            MinValueValidator(1)
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

