from rest_framework import viewsets
from apps.blog.models import Post, Tag, Category
from apps.blog.serializers import PostSerializer, TagSerializer, CategorySerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    def retrieve(self, request, *args, **kwargs):
        self.get_object().add_view()
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
