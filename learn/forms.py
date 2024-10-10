from django.forms import ModelForm
from django.forms.widgets import Select
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        widgets = {
            "area": Select(attrs={"hx-get": "", "hx-target": "", "hx-indicator": ""})
        }
