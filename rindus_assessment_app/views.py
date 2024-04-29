# from django.shortcuts import render
# from rest_framework import viewsets
# from .models import Post, Comment
# from .serializers import PostSerializer, CommentSerializer
# import requests

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from django.contrib.auth.models import User


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Manually create and save a token for the user
        token, created = Token.objects.get_or_create(user=User.objects.all()[0])
        return Response({'token': token.key})

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        try:
            # Read permissions are allowed to any request,
            # so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:
                return True

            # Write permissions are only allowed to the owner of the post.
            return obj.user_id == request.user.id
        except:
            return False


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=99999942)  # Set user_id for new posts


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]