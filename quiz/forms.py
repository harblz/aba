import datetime

from django import forms

from .models import Quiz, TrueFalseQuestion


class TakeQuizForm(forms.Form):
    answer = forms.ChoiceField(
        widget=forms.RadioSelect(),
    )

    def __init__(self, *args, **kwargs):
        choices = None
        if "choices" in kwargs:
            choices = kwargs.pop("choices")
            super(TakeQuizForm, self).__init__(*args, **kwargs)
            self.fields["answer"].choices = choices
        else:
            super(TakeQuizForm, self).__init__(*args, **kwargs)


class EditQuizForm(forms.ModelForm):
    timed = forms.BooleanField(required=False)

    class Meta:
        model = Quiz
        exclude = ["slug"]
        widgets = {
            "time": forms.NumberInput(),
            "timed": forms.CheckboxInput(
                attrs={
                    "hx-get": "/quiz/change/time",
                    "hx-target": "#id_time",
                    "hx-swap": "outerHTML",
                    # "hx-indicator": "",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EditQuizForm, self).__init__(*args, **kwargs)
        if self.instance.slug:
            if self.instance.timed:
                self.initial["time"] = int(self.instance.time.seconds / 60)
                self.fields["timed"].widget = forms.HiddenInput()
            else:
                self.fields["timed"].widget = forms.HiddenInput()
                self.fields["time"].widget = forms.HiddenInput()
        else:
            self.fields["time"].widget.attrs["hidden"] = ""
            self.fields["timed"].widget.attrs[
                "_"
            ] = "on input toggle @hidden on #id_time"

    def save(self, commit=True):
        instance = super(EditQuizForm, self).save(commit=False)
        if instance.timed:
            instance.time = datetime.timedelta(
                minutes=self.cleaned_data["time"].seconds
            )
        if commit:
            instance.save()
        return instance


class EditTrueFalseForm(forms.ModelForm):
    answer = forms.BooleanField(
        required=False, widget=forms.Select(choices=[(True, "True"), (False, "False")])
    )

    class Meta:
        model = TrueFalseQuestion
        fields = "__all__"
