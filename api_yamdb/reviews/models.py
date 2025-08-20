from django.db import models


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
