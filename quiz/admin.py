from django.contrib import admin

from .forms import EditQuizForm, EditTrueFalseForm
from .models import *


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    exclude = ["slug", "number"]
    form = EditQuizForm

    class Media:
        js = ["https://unpkg.com/hyperscript.org@0.9.13"]


class MultipleChoiceAnswerAdmin(admin.StackedInline):
    model = MultipleChoiceAnswer


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceAdmin(admin.ModelAdmin):
    exclude = ["type"]
    inlines = [MultipleChoiceAnswerAdmin]


@admin.register(TrueFalseQuestion)
class TrueFalseAdmin(admin.ModelAdmin):
    exclude = ["type"]
    form = EditTrueFalseForm


"""@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    pass"""
