from django.contrib import admin
from .models import *
from .forms import EditQuizForm


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    exclude = ["slug", "number"]
    form = EditQuizForm

    class Media:
        js = ["https://unpkg.com/hyperscript.org@0.9.13"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
