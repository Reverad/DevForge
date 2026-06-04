from django.urls import path

from tasks.views import TaskListView, TaskDetailView, TaskUpdateView, TaskDeleteView, ProjectTaskListView, \
    ProjectTaskCreateView

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("projects/<int:pk>/", ProjectTaskListView.as_view(), name="project-task-list"),
    path("projects/<int:pk>/create/", ProjectTaskCreateView.as_view(), name="project-task-create"),
]

app_name = "tasks"
