from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from teams.forms import TeamCreateForm
from teams.models import Team


class TeamsView(generic.ListView):
    model = Team
    paginate_by = 10
    template_name = "teams/team.html"
    context_object_name = "teams"

    def get_queryset(self):
        return Team.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()


class TeamCreateView(generic.CreateView):
    model = Team
    form_class = TeamCreateForm
    template_name = "teams/team_create.html"
    success_url = reverse_lazy("teams:team-list")

    def form_valid(self, form):
        team = form.save(commit=False)
        team.owner = self.request.user
        team.save()

        team.members.add(self.request.user)

        return super().form_valid(form)
