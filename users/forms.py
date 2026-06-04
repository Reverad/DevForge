from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("bio", "github")
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Tell about yourself...",
                }
            ),
            "github": forms.URLInput(
                attrs={"placeholder": "https://github.com/yourusername"}
            ),
        }
