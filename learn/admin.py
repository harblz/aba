from django.contrib import admin

from django.utils.html import format_html

from django.contrib.admin import SimpleListFilter

from .models import Course, Unit, LessonPage, Objective, TaskListItem, TaskListItemCategory, Certification, Profile, Module

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

# Register your models here.
class ModuleInline(admin.TabularInline):
    model = Module
admin.site.register(Module)

# Register your models here.
class CourseInline(admin.TabularInline):
    model = Course
admin.site.register(Course)

# Register your models here.
class ProfileInline(admin.TabularInline):
    model = Profile
admin.site.register(Profile)


# Register your models here.
class UnitInline(admin.TabularInline):
    model = Unit
admin.site.register(Unit)

# Register your models here.
class LessonPageAdmin(admin.ModelAdmin):
    save_as=True
    save_on_top=True
    view_on_site=True
    
    list_display = ['author', 'title', 'status', 'created_date', 'published_date']
    ordering = ['-published_date']
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