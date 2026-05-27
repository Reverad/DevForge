from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from teams.models import Team

User = get_user_model()


class ProjectTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="denis", password="password123")
        self.user2 = User.objects.create_user(username="sergey", password="password123")

        self.team = Team.objects.create(name="Team mate", owner=self.user1)
        self.team.members.add(self.user1)

        self.project = Project.objects.create(
            title="review",
            description="Project description",
            genre="Development",
            status="Open",
            team=self.team
        )

    def test_project_model_str(self):
        self.assertEqual(str(self.project), "review")

    def test_project_list_view_authenticated(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("projects:project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "review")
        self.assertIn(self.team, response.context["user_teams"])

    def test_project_list_view_filters(self):
        self.client.login(username="denis", password="password123")

        response = self.client.get(reverse("projects:project-list"), {"search": "review"})
        self.assertEqual(len(response.context["object_list"]), 1)

        response = self.client.get(reverse("projects:project-list"), {"search": "notfound"})
        self.assertEqual(len(response.context["object_list"]), 0)

    def test_project_detail_view(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("projects:project-detail", kwargs={"pk": self.project.pk}))

        self.assertEqual(response.status_code, 200)

    def test_project_create_view_get(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("projects:project-create"))

        self.assertEqual(response.status_code, 200)

    def test_project_update_view_owner(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("projects:project-update", kwargs={"pk": self.project.pk}))

        self.assertEqual(response.status_code, 200)

    def test_project_update_view_not_owner(self):
        self.client.login(username="sergey", password="password123")
        response = self.client.get(reverse("projects:project-update", kwargs={"pk": self.project.pk}))

        self.assertEqual(response.status_code, 404)

    def test_project_delete_view_not_owner(self):
        self.client.login(username="sergey", password="password123")
        response = self.client.post(reverse("projects:project-delete", kwargs={"pk": self.project.pk}))

        self.assertEqual(response.status_code, 404)

    def test_project_delete_view_owner(self):
        self.client.login(username="denis", password="password123")
        response = self.client.post(reverse("projects:project-delete", kwargs={"pk": self.project.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
