from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from .models import Project, Task, Bug
from django.forms.widgets import TextInput, Textarea


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class ManageAccessForm(Form):
    member = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                            required=True,
                                            label="Add member")


class TaskForm(ModelForm):
    def __init__(self, status=None, project=None, **kwargs):
        super(TaskForm, self).__init__(**kwargs)

        if project and type(project) is Project:
            self.fields["performer"].queryset = project.team
            self.fields["project"].initial = project

        if status and type(status) is str:
            self.fields["status"].initial = status

    class Meta:
        model = Task
        exclude = ("user", "recurring",)
        fields = "__all__"
        widgets = {
            "status": forms.HiddenInput(),
            "project": forms.HiddenInput(),
            "start_time": forms.HiddenInput(),
            "end_time": forms.HiddenInput(),
        }


class BugForm(ModelForm):
    def __init__(self, project=None, status=None, **kwargs):
        super(BugForm, self).__init__(**kwargs)

        if project and type(project) is Project:
            self.fields["performer"].queryset = project.team
            self.fields["project"].initial = project

        if status and type(status) is str:
            self.fields["status"].initial = status

    class Meta:
        model = Bug
        exclude = ("user", "recurring",)
        fields = "__all__"
        widgets = {
            "status": forms.HiddenInput(),
            "project": forms.HiddenInput(),
            "start_time": forms.HiddenInput(),
            "end_time": forms.HiddenInput(),
            "description": Textarea(attrs={"class": "form-control", "rows": 8}),
        }
