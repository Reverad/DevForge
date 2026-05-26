from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from projects.models import Project
from tasks.forms import TaskUpdateForm
from tasks.models import Task
from tasks.services.filter_tasks_service import filter_tasks


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 6

    def get_queryset(self):
        queryset = Task.objects.filter(
            assignees=self.request.user
        ).select_related(
            "project"
        ).prefetch_related(
            "assignees"
        )

        return filter_tasks(queryset, self.request.GET)


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


class ProjectTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 6
    template_name = "tasks/project_task_list.html"

    def get_queryset(self):
        project_pk = self.kwargs.get("pk")

        project = get_object_or_404(
            Project,
            pk=project_pk,
            team__members=self.request.user
        )

        queryset = Task.objects.filter(
            project=project
        ).select_related(
            "project", "task_type"
        ).prefetch_related(
            "assignees"
        )

        return filter_tasks(queryset, self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return context


class ProjectTaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "tasks/project_task_create.html"

    def form_valid(self, form):
        project_pk = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=project_pk, team__members=self.request.user)

        form.instance.project = project

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tasks:project-task-list", kwargs={"pk": self.kwargs.get("pk")})
