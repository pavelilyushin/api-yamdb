from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlePostMethodSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)
from reviews.models import Category, Genre, Title, Review, Comment


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('name', 'year',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostMethodSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(
            Title,
            pk=title_id
        )

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            title=title,
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('reviews_id')
        return get_object_or_404(
            Review,
            pk=review_id,
            title__id=title_id
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            review=review,
            author=self.request.user
        )
