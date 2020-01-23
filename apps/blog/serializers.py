from rest_framework import serializers
from apps.blog.models import Post, Tag, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    def to_internal_value(self, data):
        tags = data.pop('tags')
        data['tags'] = []
        for tag in tags:
            t_exists = Tag.objects.filter(id=tag).exists()
            if t_exists:
                data['tags'].append(tag)

        return super(PostSerializer, self).to_internal_value(data)

    class Meta:
        model = Post
        fields = '__all__'
