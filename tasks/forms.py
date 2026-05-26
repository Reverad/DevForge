from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from tasks.models import Task

User = get_user_model()


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "task_type",
            "tags",
            "assignees",
        ]
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        if project:
            team = project.team
            self.fields["assignees"].queryset = User.objects.filter(
                Q(id=team.owner.id) | Q(teams=team)
            ).distinct()
