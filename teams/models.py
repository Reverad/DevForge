from django.conf import settings
from django.db import models

from users.models import User


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_teams", on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams", blank=True)
