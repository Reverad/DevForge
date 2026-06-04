from django.test import TestCase
from django.contrib.auth import get_user_model
from teams.models import Team

User = get_user_model()


class TeamModelTests(TestCase):
    def setUp(self):
        self.denis = User.objects.create_user(username="denis", password="password123")
        self.team = Team.objects.create(name="Mate team", description="some description", owner=self.denis)

    def test_team_model_str(self):
        self.assertEqual(str(self.team), "Mate team")

    def test_team_absolute_url(self):
        self.assertEqual(self.team.get_absolute_url(), f"/team/{self.team.pk}/")
