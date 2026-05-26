from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from projects.forms import ProjectCreateForm
from projects.models import Project
from teams.models import Team


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.filter(
            Q(team__owner=user) | Q(team__members=user)
        ).select_related("team").distinct()

        team_id = self.request.GET.get("team")
        status = self.request.GET.get("status")
        search_query = self.request.GET.get("search")

        if team_id:
            queryset = queryset.filter(team_id=team_id)
        if status:
            queryset = queryset.filter(status=status)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["user_teams"] = Team.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "projects/project_create.html"
    success_url = reverse_lazy("projects:project-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "projects/project_update.html"

    def get_queryset(self):
        return Project.objects.filter(team__owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("projects:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("projects:project-list")

    def get_queryset(self):
        return Project.objects.filter(team__owner=self.request.user)
