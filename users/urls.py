from django.urls import path

from users.views import RegisterView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile"),
    path("edit/", ProfileUpdateView.as_view(), name="edit"),
]

app_name = "users"
