import math

from django.contrib import admin

from django.utils.html import format_html

from django.contrib.admin import SimpleListFilter

from .models import Unit, Form, Difficulty, Choice, Question, Task, QuizScore, QuizScoreSummary

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from django.db.models import Count, Avg, Sum, Min, Max, DateTimeField
from django.db.models.functions import Trunc

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

def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'

    if date_hierarchy + '__month' in request.GET:
        return 'day'

    if date_hierarchy + '__year' in request.GET:
        return 'week'

    return 'month'

@admin.register(QuizScoreSummary)
class QuizScoreSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/quiz_scores_summary.html'
    date_hierarchy = 'date'

    list_filter = (
        'date',
        'unit_id__unit_name'
    )


    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total': Count('id'),
            'average_score': Avg('score')*100,
        }

        response.context_data['summary'] = list(
            qs
            .values('unit_id__unit_name')
            .annotate(**metrics)
            .order_by('-average_score')
        )


        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period


        summary_over_time = qs.annotate(
            period=Trunc('date', period, output_field=DateTimeField()),
        ).values('period').annotate(total=Avg('score')*100).order_by('period')

        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = 100
        low = 0

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': \
               ((x['total'] or 0) - low) / (high - low) * 100
               if high > low else 0,
        } for x in summary_over_time]
        
        return response

class QuizScoreAdmin(admin.ModelAdmin):
    list_display    = ['percent_score', 'unit_id', 'form_id', 'date']
    list_filter     = ['unit_id', 'form_id', 'date']
    search_fields   = ['unit_id__unit_name', 'form_id__form_name', 'date', 'score']
    list_per_page = 100

    def percent_score(self, obj):
        return round(obj.score*100,1)
admin.site.register(QuizScore, QuizScoreAdmin)


class DifficultyInline(admin.TabularInline):

    model = Difficulty
admin.site.register(Difficulty)


def change_difficulty_RBT(modeladmin, request, queryset):

    queryset.update(difficulty='RBT')
change_difficulty_RBT.short_description = "Change selected questions difficulty to RBT"


class QuestionAdmin(admin.ModelAdmin):
    save_as=True
    save_on_top=True
    view_on_site=True
    
    readonly_fields = ('id',)
    list_display = ('id', 'escaped_question_text', 'question_unit_name', 'question_form_name', 'has_answer', 'error_reports', 'question_difficulty', 'task_list_item', 'pub_date', 'was_published_recently')
    list_per_page = 100000
    list_filter = ('unit_id', 'task_list_item', 'form_id', 'pub_date')
    #list_filter = ('unit_id', RelatedDropdownFilter) # https://github.com/mrts/django-admin-list-filter-dropdown/issues/5

    # actions = [change_unit]

    def escaped_question_text(self, obj):
        return format_html(obj.question_text)

    def question_unit_name(self, obj):
        return Unit.objects.get(pk=obj.unit_id)

    def question_form_name(self, obj):
        return Form.objects.get(pk=obj.form_id)

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
    search_fields = [ 'id', 'question_text', 'choice__choice_text', 'question_hint']
admin.site.register(Question, QuestionAdmin)
