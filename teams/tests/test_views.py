from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from teams.models import Team

User = get_user_model()


class TeamViewTests(TestCase):
    def setUp(self):
        self.denis = User.objects.create_user(username="denis", password="password123")
        self.sergey = User.objects.create_user(username="sergey", password="password123")

        self.team = Team.objects.create(name="Mate team", description="some description", owner=self.denis)
        self.team.members.add(self.denis)

    def test_teams_list_view_authenticated(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("teams:team-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mate team")

    def test_team_create_view(self):
        self.client.login(username="denis", password="password123")
        response = self.client.post(reverse("teams:team-create"), {"name": "New Team", "description": "Desc"})
        self.assertEqual(response.status_code, 302)
        new_team = Team.objects.get(name="New Team")

        self.assertEqual(new_team.owner, self.denis)
        self.assertIn(self.denis, new_team.members.all())

    def test_team_detail_view(self):
        self.client.login(username="denis", password="password123")
        response = self.client.get(reverse("teams:team-detail", kwargs={"pk": self.team.pk}))

        self.assertEqual(response.status_code, 200)

    def test_team_delete_view_owner(self):
        self.client.login(username="denis", password="password123")
        response = self.client.post(reverse("teams:team-delete", kwargs={"pk": self.team.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Team.objects.filter(pk=self.team.pk).exists())

    def test_team_delete_view_not_owner(self):
        self.client.login(username="sergey", password="password123")
        response = self.client.post(reverse("teams:team-delete", kwargs={"pk": self.team.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(pk=self.team.pk).exists())

    def test_team_add_member_success(self):
        self.client.login(username="denis", password="password123")
        response = self.client.post(reverse(
            "teams:team-add-member",
            kwargs={"pk": self.team.pk}),
            {"username": "sergey"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.sergey, self.team.members.all())

    def test_team_add_member_not_found(self):
        self.client.login(username="denis", password="password123")
        response = self.client.post(reverse(
            "teams:team-add-member",
            kwargs={"pk": self.team.pk}),
            {"username": "vadym"}
        )

        self.assertEqual(response.status_code, 302)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("User @vadym not found.", messages)

    def test_team_remove_member_success(self):
        self.team.members.add(self.sergey)
        self.client.login(username="denis", password="password123")
        response = self.client.post(reverse(
            "teams:team-remove-member",
            kwargs={"pk": self.team.pk}),
            {"member_id": self.sergey.id}
        )

        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.sergey, self.team.members.all())

    def test_team_remove_owner_error(self):
        self.client.login(username="denis", password="password123")
        response = self.client.post(reverse(
            "teams:team-remove-member",
            kwargs={"pk": self.team.pk}),
            {"member_id": self.denis.id}
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.denis, self.team.members.all())

    def test_team_update_description_owner(self):
        self.client.login(username="denis", password="password123")
        response = self.client.post(reverse(
            "teams:team-update-description",
            kwargs={"pk": self.team.pk}),
            {"description": "New description text"}
        )

        self.assertEqual(response.status_code, 302)
        self.team.refresh_from_db()
        self.assertEqual(self.team.description, "New description text")
