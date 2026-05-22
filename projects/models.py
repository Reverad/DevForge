from django.db import models
from teams.models import Team


STATUS_CHOICES = [
    ("Open", "Open"),
    ("Closed", "Closed"),
]

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
    )
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title
