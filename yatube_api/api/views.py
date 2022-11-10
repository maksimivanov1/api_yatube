from .permissions import IsAuthorOrReadOnly

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny


from django.shortcuts import get_object_or_404

from posts.models import Group, Post
from .serializers import CommentViewSerializer, GroupViewSerializer, PostViewSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostViewSerializer
    permission_classes = IsAuthenticated, IsAuthorOrReadOnly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupViewSerializer
    permission_classes = IsAuthenticated, AllowAny


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentViewSerializer
    permission_classes = IsAuthenticated, IsAuthorOrReadOnly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments
