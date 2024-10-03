from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    exclude = ["slug"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
