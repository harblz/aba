from django.contrib import admin
from .models import QuizQuestion, QuizChoice

# Registered models
admin.site.register(QuizQuestion)
admin.site.register(QuizChoice)
