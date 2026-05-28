from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project
from teams.models import Team
from tasks.models import Task, TaskType, Tag

User = get_user_model()


class TaskModelTests(TestCase):
    def setUp(self):
        self.denis = User.objects.create_user(username="denis", password="password123")
        self.team = Team.objects.create(name="Mate team", owner=self.denis)
        self.project = Project.objects.create(title="review", team=self.team)

        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="Backend")

        self.task = Task.objects.create(
            title="find issue",
            description="Fix this critical bug",
            project=self.project,
            task_type=self.task_type
        )

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Bug")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Backend")

    def test_task_str(self):
        self.assertEqual(str(self.task), "find issue")

    def test_task_default_values(self):
        self.assertEqual(self.task.priority, "Medium")
        self.assertEqual(self.task.status, "Open")
