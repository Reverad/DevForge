from django.conf import settings
from django.db import models

from projects.models import STATUS_CHOICES, Project


PRIORITY_CHOICES = [
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("High", "High"),
]

class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "TaskTypes"
        verbose_name = "TaskType"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES[1][0])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, related_name="tasks", blank=True, null=True)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks", blank=True)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    class Meta:
        verbose_name_plural = "Tasks"
        verbose_name = "Task"
        ordering = ["-due_date"]

    def __str__(self):
        return self.title
