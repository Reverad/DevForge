from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Position

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="python developer")

        self.user1 = User.objects.create_user(
            username="denis",
            password="password123",
            first_name="denis",
            last_name="dymerlii",
            email="mate@example.com",
            bio="...",
            github="https://github.com/mateacademy",
            position=self.position
        )
        self.user2 = User.objects.create_user(
            username="sergey",
            password="password123",
            first_name="sergey",
            last_name="leonenko",
            email="mate@example.com"
        )

    def test_position_model_str(self):
        self.assertEqual(str(self.position), "python developer")

    def test_user_model_str(self):
        self.assertEqual(str(self.user1), "denis")

    def test_register_view_get(self):
        response = self.client.get(reverse("users:register"))

        self.assertEqual(response.status_code, 200)

    def test_profile_detail_view_own_profile(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("users:profile", kwargs={"pk": self.user1.pk}))

        self.assertEqual(response.status_code, 200)

        profile_user = response.context["profile_user"]
        self.assertEqual(profile_user.first_name, "denis")
        self.assertEqual(profile_user.last_name, "dymerlii")
        self.assertEqual(profile_user.email, "mate@example.com")

    def test_profile_detail_view_other_profile_hides_info(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("users:profile", kwargs={"pk": self.user2.pk}))

        self.assertEqual(response.status_code, 200)

        profile_user = response.context["profile_user"]
        self.assertEqual(profile_user.first_name, "")
        self.assertEqual(profile_user.last_name, "")
        self.assertEqual(profile_user.email, "")

    def test_profile_update_view_get(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("users:edit"))

        self.assertEqual(response.status_code, 200)

    def test_profile_update_view_post(self):
        self.client.login(username="denis", password="password123")
        data = {
            "first_name": "new",
            "last_name": "new",
            "email": "new@example.com",
            "bio": "...",
            "github": "https://github.com/new"
        }

        response = self.client.post(reverse("users:edit"), data)
        self.assertEqual(response.status_code, 302)

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "new")
        self.assertEqual(self.user1.bio, "...")
