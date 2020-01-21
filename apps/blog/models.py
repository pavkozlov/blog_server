from django.db import models


class Post(models.Model):
    # Заголовок
    title = models.CharField(max_length=150, db_index=True, unique=True, blank=False, null=False)
    # Тело
    body = models.TextField(db_index=True, blank=False, null=False)
    # Теги
    tags = models.ManyToManyField('Tag', related_name='tag_posts', db_index=True, blank=True, default=[])
    # Категория
    category = models.ForeignKey(
        'Category',
        related_name='category_posts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    # СЛУЖЕБНЫЕ
    # Дата создания
    created = models.DateTimeField(auto_now_add=True)
    # Просмотры
    views = models.BigIntegerField(default=0, blank=False, null=False)

    def add_view(self):
        self.views += 1
        self.save()


class Tag(models.Model):
    # Заголовок
    title = models.CharField(max_length=150, unique=True, blank=False, null=False)


class Category(models.Model):
    # Заголовок
    title = models.CharField(max_length=150, unique=True, blank=False, null=False)
