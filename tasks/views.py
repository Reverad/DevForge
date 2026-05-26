from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskUpdateForm
from tasks.models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 6

    def get_queryset(self):
        queryset = Task.objects.filter(assignees=self.request.user).select_related("project")

        search_query = self.request.GET.get("search")

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(
            Q(project__team__owner=self.request.user) |
            Q(project__team__members=self.request.user)
        ).distinct()


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "tasks/task_update.html"

    def get_queryset(self):
        return Task.objects.filter(project__team__owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.get_object().project
        return kwargs

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")

    def get_queryset(self):
        return Task.objects.filter(project__team__owner=self.request.user)
