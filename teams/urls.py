from django.urls import path

from teams.views import (
    TeamsView,
    TeamCreateView,
    TeamDetailView,
    TeamDeleteView,
    TeamAddMemberView,
    TeamRemoveMemberView,
    TeamUpdateDescriptionView,
)


urlpatterns = [
    path("", TeamsView.as_view(), name="team-list"),
    path("create/", TeamCreateView.as_view(), name="team-create"),
    path("<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
    path("<int:pk>/add/", TeamAddMemberView.as_view(), name="team-add-member"),
    path("<int:pk>/remove/", TeamRemoveMemberView.as_view(), name="team-remove-member"),
    path( "<int:pk>/update/", TeamUpdateDescriptionView.as_view(), name="team-update-description"),
]

app_name = "teams"
