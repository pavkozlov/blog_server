# Generated by Django 3.0.2 on 2020-01-21 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200121_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, db_index=True, default=[], related_name='tag_posts', to='blog.Tag'),
        ),
    ]
