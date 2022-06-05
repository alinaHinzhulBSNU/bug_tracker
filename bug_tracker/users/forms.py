from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


def get_groups_names():
    groups = Group.objects.all().values_list('name', flat=True)
    return zip(groups, groups)


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    role = forms.ChoiceField(
        required=True,
        choices=get_groups_names(),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
