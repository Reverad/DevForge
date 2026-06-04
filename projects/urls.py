from django.urls import path

from projects.views import ProjectListView, ProjectCreateView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    path("", ProjectListView.as_view(), name="project-list"),
    path("create/", ProjectCreateView.as_view(), name="project-create"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("update/<int:pk>/", ProjectUpdateView.as_view(), name="project-update"),
    path("delete/<int:pk>/", ProjectDeleteView.as_view(), name="project-delete"),
]

app_name = "projects"
