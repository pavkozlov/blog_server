from rest_framework import serializers
from apps.blog.models import Post, Tag, Category


class TagSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, *args):
        return Post.objects.filter(tags__in=[args[0]]).count()

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, *args):
        return Post.objects.filter(category=args[0]).count()

    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.ListField(write_only=True, required=False, default=[])
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        allow_null=True,
        default=None
    )

    def create(self, validated_data):
        tags = validated_data.pop('tags_ids')
        post = Post.objects.create(**validated_data)
        for tag in tags:
            tags_list = Tag.objects.filter(id=tag)
            if tags_list.exists():
                tag_obj = tags_list.first()
                post.tags.add(tag_obj)
        post.save()
        return post

    class Meta:
        model = Post
        fields = '__all__'
