from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
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
