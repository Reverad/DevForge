from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("user/", include("users.urls", namespace="users")),
    path("team/", include("teams.urls", namespace="teams")),
    path("project/", include("projects.urls", namespace="projects")),
    # path("task/", include("tasks.urls", namespace="tasks")),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
