from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter
from .serializers import (
    CategorySerializer, GenreSerializer, TitlePostMethodSerializer, TitleSerializer
)
from reviews.models import Category, Genre, Title


class CreateDestroyListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('name', 'year', 'category', 'genre')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostMethodSerializer
