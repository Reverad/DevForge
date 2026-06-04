from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from tasks.models import Task
from teams.models import Team

User = get_user_model()


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="denis", password="password123")

        self.team = Team.objects.create(name="Mate team", owner=self.user)
        self.team.members.add(self.user)

        self.project = Project.objects.create(title="review", team=self.team)

        self.task = Task.objects.create(title="find issue", project=self.project)
        self.task.assignees.add(self.user)

        self.index_url = reverse("core:index")

    def test_index_view_redirects_anonymous_user(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 302)

    def test_index_view_success_for_authenticated_user(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")

    def test_index_view_context_counters(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(self.index_url)

        self.assertEqual(response.context["total_projects"], 1)
        self.assertEqual(response.context["total_tasks"], 1)
        self.assertEqual(response.context["total_teams"], 1)

    def test_index_view_context_counters_for_empty_user(self):
        User.objects.create_user(username="sergey", password="password123")
        self.client.login(username="sergey", password="password123")
        response = self.client.get(self.index_url)

        self.assertEqual(response.context["total_projects"], 0)
        self.assertEqual(response.context["total_tasks"], 0)
        self.assertEqual(response.context["total_teams"], 0)
