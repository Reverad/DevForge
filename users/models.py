from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Positions"
        verbose_name = "Position"

    def __str__(self):
        return self.name


class User(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    github = models.URLField(max_length=255, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"

    def __str__(self):
        return self.username
