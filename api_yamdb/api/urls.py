from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, SignUpView, TokenView
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/', include([
        path('', include(router_v1.urls)),
        path('auth/signup/', SignUpView.as_view(), name='signup_v1'),
        path('auth/token/', TokenView.as_view(), name='token_v1'),
    ])),
]
