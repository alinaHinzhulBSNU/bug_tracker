from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from .models import Project, Task
from django.forms.widgets import TextInput, Textarea


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description")
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class TaskForm(ModelForm):
    def __init__(self, project=None, **kwargs):
        super(TaskForm, self).__init__(**kwargs)
        if project and type(project) is Project:
            self.fields["performer"].queryset = project.team

    class Meta:
        model = Task
        exclude = ("user", "recurring",)
        fields = ("text", "severity", "status", "performer")


class ManageAccessForm(Form):
    member = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                            required=True,
                                            label="Add member")
