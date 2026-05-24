from django import forms

from teams.models import Team


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "description")
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your team name"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "What does your team do?",
                "rows": 4
            }),
        }
