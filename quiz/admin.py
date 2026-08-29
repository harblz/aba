from django.contrib import admin
from django.forms import Script

from core.utilities import generate_color_palette
from .forms import EditQuizForm, EditTrueFalseForm
from .models import *


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    exclude = ["slug", "number"]
    form = EditQuizForm


class MultipleChoiceAnswerAdmin(admin.StackedInline):
    model = MultipleChoiceAnswer


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceAdmin(admin.ModelAdmin):
    exclude = ["type"]
    inlines = [MultipleChoiceAnswerAdmin]

    def change_view(self, request, object_id, form_url="", extra_context=None):
        question = MultipleChoiceQuestion.objects.prefetch_related("answers").get(id=object_id)
        answers = question.answers.all()
        data = []
        for answer in answers:
            data.append(answer.picked)

        chart_data = {
            "labels":[chr(i) for i in range(97, 97 + len(data))],
            "datasets":[{
                "label": "Times picked",
                "data": data,
                "backgroundColor": generate_color_palette(len(data)),
            }]

        }
        extra_context = extra_context or {}
        extra_context["chart_data"] = chart_data
        return super().change_view(request, object_id, form_url, extra_context)


    class Media:
        js = ["js/chart.js"]



@admin.register(TrueFalseQuestion)
class TrueFalseAdmin(admin.ModelAdmin):
    exclude = ["type"]
    form = EditTrueFalseForm


"""@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    pass"""
