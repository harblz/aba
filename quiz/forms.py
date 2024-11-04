import datetime

from django import forms


class TakeQuizForm(forms.Form):
    question = forms.Textarea()
    answer = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, question, *args, **kwargs):
        super(TakeQuizForm, self).__init__(*args, **kwargs)
        self.question = question.text
        choices = (question.one, question.two, question.three, question.four)
        letters = ("A", "B", "C", "D")
        self.answer.choices = {}
        for index, choice in enumerate(choices):
            if choice:
                self.answer.choices[letters[index]] = choice
            else:
                break


class EditQuizForm(forms.ModelForm):
    timed = forms.BooleanField(required=False)

    class Meta:
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
