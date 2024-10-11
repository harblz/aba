from django.forms import ModelForm
from django.forms.widgets import Select
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ["slug"]
        widgets = {
            "license": Select(
                attrs={
                    "hx-get": "/learn/task/change/options",
                    "hx-target": "#id_area",
                    "hx-swap": "outerHTML",
                    # "hx-indicator": "",
                }
            )
        }
