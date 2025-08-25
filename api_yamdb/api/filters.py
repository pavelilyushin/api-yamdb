import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')
    name = django_filters.CharFilter(field_name='name')
    year = django_filters.CharFilter(field_name='year')

# Стандартные поля избыточно в полях указывать. Достаточно в Мета

    class Meta:
        model = Title
        fields = ('category', 'genre')
