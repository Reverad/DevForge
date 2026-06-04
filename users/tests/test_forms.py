from django.test import TestCase
from users.forms import RegisterForm


class RegisterFormTests(TestCase):
    def test_register_form_valid_data(self):
        data = {
            "username": "denis_valid",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "bio": "Backend dev",
            "github": "https://github.com/mateacademy"
        }
        form = RegisterForm(data=data)

        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        data = {
            "username": "",
            "password1": "StrongPass123!",
            "password2": "DifferentPass123!",
            "bio": "...",
            "github": "invalid-url"
        }
        form = RegisterForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password2", form.errors)
        self.assertIn("github", form.errors)
