from django import forms


class QuizForm(forms.Form):
    question = forms.Textarea()
    answer = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, question, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.question = question.text
        choices = (question.one, question.two, question.three, question.four)
        letters = ("A", "B", "C", "D")
        self.answer.choices = {}
        for index, choice in enumerate(choices):
            if choice:
                self.answer.choices[letters[index]] = choice
            else:
                break
