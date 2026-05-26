from django.urls import path

from tasks.views import TaskListView, TaskDetailView

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]

app_name = "tasks"
