from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Position

User = get_user_model()


class UserModelTests(TestCase):
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

    def test_position_model_str(self):
        self.assertEqual(str(self.position), "python developer")

    def test_user_model_str(self):
        self.assertEqual(str(self.user1), "denis")
