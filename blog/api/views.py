from rest_framework.generics import (
        RetrieveUpdateAPIView,
        CreateAPIView,
        ListAPIView,
        RetrieveAPIView,
        DestroyAPIView,
    )

from .serializers import (
        PostListSerializer,
        PostDetailSerializer,
        PostCreateSerializer,

    )

from rest_framework.permissions import (
        AllowAny,
        IsAdminUser,
        IsAuthenticated,


    )

from blog.models import Post
from .permissions import IsOwnerOrReadOnly


class PostCreateAPIView(CreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListAPIView(ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.published.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.published.all()
    serializer_class = PostCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(aurhor=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.published.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

