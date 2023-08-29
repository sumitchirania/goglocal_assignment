import jwt

from django.conf import settings

from datetime import datetime, timedelta

from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password


class User(AbstractBaseUser):

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    username = models.CharField(max_length=256, unique=True)

    USERNAME_FIELD = 'username'
    
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name}" + f" {self.last_name}"

