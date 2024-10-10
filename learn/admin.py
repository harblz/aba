from django.contrib import admin
from learn.models import *


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


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
    fields = ["license", "area", "task", "task_desc"]
    autocomplete_fields = ["area"]
    formfield_overrides = {}


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
