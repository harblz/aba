from django.contrib import admin
from .models import *
from .forms import EditQuizForm


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    exclude = ["slug"]
    form = EditQuizForm


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
