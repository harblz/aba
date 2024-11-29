from django.contrib import admin

import quiz.forms
from .models import *
from .forms import EditQuizForm, EditTrueFalseForm


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    exclude = ["slug", "number"]
    form = EditQuizForm

    class Media:
        js = ["https://unpkg.com/hyperscript.org@0.9.13"]


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(MultipleChoiceAnswer)
class MultipleChoiceAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(TrueFalseQuestion)
class TrueFalseAdmin(admin.ModelAdmin):
    form = EditTrueFalseForm
