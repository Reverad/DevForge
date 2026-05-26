from django import forms

from projects.models import Project
from teams.models import Team


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "genre", "status", "deadline", "team"]
        widgets = {
            "deadline": forms.DateInput(
                attrs={
                    "placeholder": "YYYY-MM-DD",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["team"].queryset = Team.objects.filter(owner=user)
