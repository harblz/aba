from django.contrib import admin
from .models import *
from .forms import TaskForm


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(ContentArea)
class ContentAreaAdmin(admin.ModelAdmin):
    ordering = ["slug"]
    fields = ["license", "section", ("letter", "area"), "weight"]
    search_fields = ["slug"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskForm

    class Media:
        js = ("js/htmx.min.js", "django-htmx.js")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
