from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostViewSet, CommentViewSet, CustomAuthToken


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', CustomAuthToken.as_view(), name='token_obtain_pair'),
]