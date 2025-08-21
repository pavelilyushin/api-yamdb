from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, signup, token

from .views import (UserViewSet,
                    signup,
                    token,
                    CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet
)
router = DefaultRouter()
router.register('users', UserViewSet)
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
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token'),
    path('v1/', include(router_v1.urls)),
]
