from django.contrib import admin

from django.utils.html import format_html

from django.contrib.admin import SimpleListFilter

from .models import Unit, Difficulty, Choice, Question, Task

# Extending SimpleListFilter

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class UnitInline(admin.TabularInline):
    model = Unit
admin.site.register(Unit)


class TaskInline(admin.TabularInline):
    model = Task
admin.site.register(Task)


class DifficultyInline(admin.TabularInline):
    model = Difficulty
admin.site.register(Difficulty)


def change_difficulty_RBT(modeladmin, request, queryset):
    queryset.update(difficulty='RBT')
change_difficulty_RBT.short_description = "Change selected questions difficulty to RBT"


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('escaped_question_text', 'question_unit_name', 'has_answer', 'question_difficulty', 'task_list_item', 'unit_id', 'pub_date', 'was_published_recently')
    list_per_page = 100000
    list_filter = ['unit_id', 'task_list_item', 'pub_date', ]

    # actions = [change_unit]

    def escaped_question_text(self, obj):
        return format_html(obj.question_text)

    def question_unit_name(self, obj):
        return Unit.objects.get(pk=obj.unit_id)

    def has_answer(self, obj):
        choices = Choice.objects.filter(question_id=obj.id)
        status  = False;

        for choice in choices:
            if choice.is_correct is True:
                status = True;
        
        return status;

    def question_difficulty(self, obj):
        return Difficulty.objects.get(pk=obj.difficulty_id)

    def task_name(self, obj):
        return Task.objects.get(pk=obj.task_list_item)

    escaped_question_text.allow_tags = True
    escaped_question_text.short_description = 'Question text'
    
    fieldsets = [
        (None,               {'fields': ['question_text', 'task_list_item']}),
        ('Question Hint', {'fields': ['question_hint'], 'classes': ['']}), # put "collapse" in classes to auto-hide it; requires bootstrap
        ('Unit / Course Information', {'fields': [ 'unit'], 'classes': ['']}),
        ('Difficulty', {'fields': [ 'difficulty'], 'classes': ['']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['']}),
    ]
    inlines = [ChoiceInline]
    search_fields = [  'question_text' ]
admin.site.register(Question, QuestionAdmin)
