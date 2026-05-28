from django.test import TestCase
from django.contrib.auth import get_user_model
from teams.models import Team
from projects.forms import ProjectCreateForm

User = get_user_model()


class ProjectCreateFormTests(TestCase):
    def setUp(self):
        self.denis = User.objects.create_user(username="denis", password="password123")
        self.sergey = User.objects.create_user(username="sergey", password="password123")

        self.team_denis = Team.objects.create(name="Mate team", owner=self.denis)
        self.team_sergey = Team.objects.create(name="Sergey team", owner=self.sergey)

    def test_project_form_valid_data(self):
        data = {
            "title": "review",
            "description": "Form test",
            "genre": "Development",
            "status": "Open",
            "deadline": "2026-12-31",
            "team": self.team_denis.id
        }
        form = ProjectCreateForm(data=data, user=self.denis)

        self.assertTrue(form.is_valid())

    def test_project_form_invalid_data(self):
        data = {
            "title": "",
            "description": "No title"
        }
        form = ProjectCreateForm(data=data, user=self.denis)

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_project_form_team_queryset_includes_only_owned_teams(self):
        form = ProjectCreateForm(user=self.denis)
        team_queryset = form.fields["team"].queryset

        self.assertIn(self.team_denis, team_queryset)
        self.assertNotIn(self.team_sergey, team_queryset)
