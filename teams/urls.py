from django.urls import path

from teams.views import TeamsView, TeamCreateView, TeamDetailView

urlpatterns = [
    path("", TeamsView.as_view(), name="team-list"),
    path("create/", TeamCreateView.as_view(), name="team-create"),
    path("<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
]

app_name = "teams"
