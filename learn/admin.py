from django.contrib import admin
from learn.models import *


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    exclude = ["slug"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
