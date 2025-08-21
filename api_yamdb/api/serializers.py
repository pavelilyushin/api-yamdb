from rest_framework import serializers
import datetime as dt

from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug,
        }
        data['genre'] = [{
            'name': genre.name,
            'slug': genre.slug
        } for genre in instance.genre.all()]
        return data


class TitlePostMethodSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
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
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def to_representation(self, instance):
        return TitleSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'review_author', 'review_title', 'review_pub_date',
                  'review_text')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'comment_author', 'comment_pub_date', 'comment_text')
