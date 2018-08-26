from django.contrib import admin

from django.utils.html import format_html

from django.contrib.admin import SimpleListFilter

from .models import Unit, Form, Difficulty, Choice, Question, Task

# Extending SimpleListFilter

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class UnitInline(admin.TabularInline):
    model = Unit
admin.site.register(Unit)


class FormAdmin(admin.ModelAdmin):
    list_display = ['form_name', 'form_short_name', 'form_unit_id', 'form_description']
    list_per_page = 100000
    list_filter  = ['form_name', 'form_unit_id']
    search_fields = [  'form_name', 'form_description' ]

admin.site.register(Form, FormAdmin)


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
    list_display = ('escaped_question_text', 'question_unit_name', 'question_form_name', 'has_answer', 'question_difficulty', 'task_list_item', 'pub_date', 'was_published_recently')
    list_per_page = 100000
    list_filter = ['unit_id', 'task_list_item', 'form_id', 'pub_date', ]

    # actions = [change_unit]

    def escaped_question_text(self, obj):
        return format_html(obj.question_text)

    def question_unit_name(self, obj):
        return Unit.objects.get(pk=obj.unit_id)

    def question_form_name(self, obj):
        return Form.objects.get(pk=obj.unit_id)

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

    question_form_name.short_description    = 'Form'
    question_form_name.admin_order_field    = 'form__form_name'

    question_unit_name.short_description    = 'Unit'
    question_unit_name.admin_order_field    = 'unit__unit_name'

    question_difficulty.short_description   = 'Difficulty'


    has_answer.admin_order_field            = 'choice__is_correct'
    question_difficulty.admin_order_field   = 'difficulty__difficulty_name'
    
    fieldsets = [
        (None,               {'fields': ['question_text', 'task_list_item']}),
        ('Question Hint', {'fields': ['question_hint'], 'classes': ['']}), # put "collapse" in classes to auto-hide it; requires bootstrap
        ('Unit / Course Information', {'fields': [ 'unit', 'form' ], 'classes': ['']}),
        ('Difficulty', {'fields': [ 'difficulty'], 'classes': ['']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['']}),
    ]
    inlines = [ChoiceInline]
    search_fields = [  'question_text' ]
admin.site.register(Question, QuestionAdmin)
