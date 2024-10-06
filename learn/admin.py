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
    change_form_template = "learn/change_form.html"

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        query = Course.objects.all().values("code", "name")
        licenses = {}
        for entry in query:
            if (
                entry["code"] == "RBT"
                or entry["code"] == "BCBA"
                or entry["code"] == "BCaBA"
            ):
                licenses[entry["code"]] = entry["name"]
            else:
                pass
        extra_context["licenses"] = licenses
        return super(TaskAdmin, self).changeform_view(
            request, object_id, form_url=form_url, extra_context=extra_context
        )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
