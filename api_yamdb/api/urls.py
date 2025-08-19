"""Root API URL routes using DRF router and auth endpoints."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, signup, token

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token'),
]
