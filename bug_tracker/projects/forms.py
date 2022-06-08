from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from .models import Project
from django.forms.widgets import TextInput, Textarea, SelectMultiple


class CreateProject(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ManageAccessForm(Form):
    member = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                            required=True,
                                            label="Add member")
