from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task
from projects.models import Project
from tasks.services.filter_tasks_service import filter_tasks
from teams.models import Team


User = get_user_model()

class DevForgeViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="denis", password="password123")
        self.other_user = User.objects.create_user(username="sergey", password="password123")

        self.team = Team.objects.create(name="Mate team", owner=self.user)
        self.team.members.add(self.user)

        self.project = Project.objects.create(
            title="DevForge Project",
            team=self.team,
            status="active"
        )

        self.task = Task.objects.create(
            title="Fix N+1 Problem",
            description="Need to add select_related",
            project=self.project,
            priority="High"
        )
        self.task.assignees.add(self.user)

    def test_dashboard_accessible_by_logged_in_user(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_redirects_anonymous_user(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 302)

    def test_project_task_list_accessible_by_team_member(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("tasks:project-task-list", kwargs={"pk": self.project.pk}))
        self.assertEqual(response.status_code, 200)

    def test_project_task_list_restricted_for_non_member(self):
        self.client.login(username="sergey", password="password123")
        response = self.client.get(reverse("tasks:project-task-list", kwargs={"pk": self.project.pk}))
        self.assertEqual(response.status_code, 404)

    def test_filter_tasks_service_by_priority(self):
        low_task = Task.objects.create(
            title="Low priority task",
            project=self.project,
            priority="Low"
        )

        get_params = QueryDict("priority=High")
        queryset = Task.objects.all()

        filtered_qs = filter_tasks(queryset, get_params)

        self.assertIn(self.task, filtered_qs)
        self.assertNotIn(low_task, filtered_qs)
