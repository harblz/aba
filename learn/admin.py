from django.contrib import admin

from django.utils.html import format_html

from django.contrib.admin import SimpleListFilter

from .models import Course, Unit, LessonPage, Objective, TaskListItem, TaskListItemCategory, Certification

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

# Register your models here.
class CourseInline(admin.TabularInline):
    model = Course
admin.site.register(Course)

# Register your models here.
class UnitInline(admin.TabularInline):
    model = Unit
admin.site.register(Unit)

# Register your models here.
class LessonPageInline(admin.TabularInline):
    save_as=True
    save_on_top=True
    view_on_site=True
    
    model = LessonPage
admin.site.register(LessonPage)

# Register your models here.
class ObjectiveInline(admin.TabularInline):
    model = Objective
admin.site.register(Objective)

# Register your models here.
class TaskListItemCategoryInline(admin.TabularInline):
    model = TaskListItemCategory
admin.site.register(TaskListItemCategory)

# Register your models here.
class TaskListItemInline(admin.TabularInline):
    model = TaskListItem
admin.site.register(TaskListItem)

# Register your models here.
class CertificationInline(admin.TabularInline):
    model = Certification
admin.site.register(Certification)