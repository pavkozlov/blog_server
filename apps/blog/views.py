from rest_framework import views, generics, viewsets
from apps.blog.models import Post
from apps.blog.serializers import PostSerializer
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        post.add_view()
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)

