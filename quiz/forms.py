import datetime
from django import forms

from .models import Quiz, TrueFalseQuestion


class TakeQuizForm(forms.Form):
    question = forms.Textarea()
    answer = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, question, *args, **kwargs):
        super(TakeQuizForm, self).__init__(*args, **kwargs)
        self.question = question.text
        choices = []
        if type(question.answer) == str:
            for index, answer in enumerate(question.answers.values()):
                choices.append((index, answer["id"], answer["text"]))
            letters = ("A", "B", "C", "D")
            for index, choice in enumerate(choices):
                if choice:
                    self.answer.choices[letters[index]] = choice
                else:
                    break
        elif type(question.answer) == bool:
            choices = [(True, "True"), (False, "False")]
        self.answer.choices = choices


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
