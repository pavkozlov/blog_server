from rest_framework import viewsets
from apps.blog.models import Post, Tag, Category
from apps.blog.serializers import PostSerializer, TagSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['created', 'views']
    filterset_fields = ['category']

    def retrieve(self, request, *args, **kwargs):
        self.get_object().add_view()
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['id']

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['id']

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
