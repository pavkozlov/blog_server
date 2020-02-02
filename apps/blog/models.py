from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    body = models.TextField(db_index=True, blank=False, null=False)
    tags = models.ManyToManyField('Tag', related_name='tag_posts', db_index=True, blank=True, default=[])
    category = models.ForeignKey(
        'Category',
        related_name='category_posts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    # СЛУЖЕБНЫЕ
    created = models.DateTimeField(auto_now_add=True)
    views = models.BigIntegerField(default=0, blank=False, null=False)
    author = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.SET_NULL)

    def add_view(self):
        self.views += 1
        self.save()


class Tag(models.Model):
    title = models.CharField(max_length=150, unique=True, blank=False, null=False)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, blank=False, null=False)
