from rest_framework import serializers
from apps.blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
