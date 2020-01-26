from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.authorization.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
