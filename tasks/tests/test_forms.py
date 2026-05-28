from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project
from teams.models import Team
from tasks.forms import TaskUpdateForm

User = get_user_model()


class TaskUpdateFormTests(TestCase):
    def setUp(self):
        self.denis = User.objects.create_user(username="denis", password="password123")
        self.sergey = User.objects.create_user(username="sergey", password="password123")

        self.team = Team.objects.create(name="Mate team", owner=self.denis)
        self.team.members.add(self.denis)

        self.project = Project.objects.create(title="review", team=self.team)

    def test_task_form_valid_data(self):
        data = {
            "title": "find issue",
            "description": "Fix it fast",
            "priority": "Medium",
            "status": "Open",
            "assignees": [self.denis.id]
        }
        form = TaskUpdateForm(data=data, project=self.project)
        
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_data(self):
        data = {
            "title": "",
            "description": "No title task"
        }
        form = TaskUpdateForm(data=data, project=self.project)

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_task_form_assignees_queryset_includes_only_team_members(self):
        form = TaskUpdateForm(project=self.project)
        assignees_queryset = form.fields["assignees"].queryset

        self.assertIn(self.denis, assignees_queryset)
        self.assertNotIn(self.sergey, assignees_queryset)
