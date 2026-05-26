from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import generic

from tasks.models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user).select_related("project")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(
            Q(project__team__owner=self.request.user) |
            Q(project__team__members=self.request.user)
        ).distinct()
