from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from projects.models import Project
from tasks.models import Task
from teams.models import Team


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["total_projects"] = Project.objects.filter(team__members=user).count()
        context["total_tasks"] = Task.objects.filter(assignees=user).count()
        context["total_teams"] = Team.objects.filter(members=user).count()

        return context
