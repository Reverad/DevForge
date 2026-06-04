from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic

from users.forms import RegisterForm


User = get_user_model()

class RegisterView(generic.CreateView):
    model = User
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile_user = context["profile_user"]
        current_user = self.request.user

        if current_user != profile_user:
            profile_user.first_name = ""
            profile_user.last_name = ""
            profile_user.email = ""

        return context


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ("first_name", "last_name", "email", "bio", "github")
    template_name = "users/edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("users:profile", kwargs={"pk": self.object.pk})
