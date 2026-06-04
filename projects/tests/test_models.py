from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project
from teams.models import Team

User = get_user_model()

class ProjectModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="denis", password="password123")
        self.team = Team.objects.create(name="Team mate", owner=self.user1)
        self.project = Project.objects.create(
            title="review",
            description="Project description",
            genre="Development",
            status="Open",
            team=self.team
        )

    def test_project_model_str(self):
        self.assertEqual(str(self.project), "review")
