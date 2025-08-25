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

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/signup/', SignUpView.as_view(), name='signup'),
    # path('auth/token/', TokenView.as_view(), name='token'),
    path('v1/', include([
        path('', include(router.urls)),
        path('auth/signup/', SignUpView.as_view(), name='signup_v1'),
        path('auth/token/', TokenView.as_view(), name='token_v1'),
    ])),
]
