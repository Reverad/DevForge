from django.test import TestCase
from teams.forms import TeamCreateForm

class TeamCreateFormTests(TestCase):
    def test_team_create_form_valid_data(self):
        data = {
            "name": "Mate team",
            "description": "Forming the best dev team ever"
        }
        form = TeamCreateForm(data=data)

        self.assertTrue(form.is_valid())

    def test_team_create_form_invalid_data(self):
        data = {
            "name": "",
            "description": "Some description"
        }
        form = TeamCreateForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
