from django.urls import path

from teams.views import TeamsView, TeamCreateView

urlpatterns = [
    path("", TeamsView.as_view(), name="team-list"),
    path("create/", TeamCreateView.as_view(), name="team-create"),
]

app_name = "teams"
