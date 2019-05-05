from django.contrib import admin

from django.utils.html import format_html

from django.contrib.admin import SimpleListFilter

from .models import Course

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter


# Register your models here.
class CourseInline(admin.TabularInline):
    model = Course
admin.site.register(Course)