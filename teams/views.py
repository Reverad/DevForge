from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views import generic

from teams.forms import TeamCreateForm
from teams.models import Team


User = get_user_model()

class TeamsView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 9
    template_name = "teams/team.html"
    context_object_name = "teams"

    def get_queryset(self):
        return Team.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreateForm
    template_name = "teams/team_create.html"

    def form_valid(self, form):
        team = form.save(commit=False)
        team.owner = self.request.user
        team.save()

        team.members.add(self.request.user)

        return super().form_valid(form)


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def post(self, request, *args, **kwargs):
        self.object: Team = self.get_object()
        team = self.object

        if team.owner != request.user:
            messages.error(request, "You do not have permission to perform this action.")
            return redirect(team.get_absolute_url())

        if "delete_team" in request.POST:
            team_name = team.name
            team.delete()
            messages.success(request, f"Team \"{team_name}\" has been successfully deleted.")
            return redirect("teams:team-list")

        elif "username" in request.POST:
            username = request.POST.get("username").strip()
            try:
                user_to_add = User.objects.get(username=username)

                if user_to_add in team.members.all():
                    messages.warning(request, f"User @{username} is already a member of this team.")
                else:
                    team.members.add(user_to_add)
                    messages.success(request, f"User @{username} has been successfully added!")
            except User.DoesNotExist:
                messages.error(request, f"User @{username} not found.")

        elif "member_id" in request.POST:
            member_id = request.POST.get("member_id")
            user_to_kick = get_object_or_404(User, id=member_id)

            if user_to_kick == team.owner:
                messages.error(request, "You cannot kick the team owner.")
            else:
                team.members.remove(user_to_kick)
                messages.success(request, f"User @{user_to_kick.username} has been removed from the team.")

        elif "description" in request.POST:
            new_description = request.POST.get("description").strip()
            team.description = new_description
            team.save()
            messages.success(request, "Team description has been successfully updated.")

        return redirect(team.get_absolute_url())
