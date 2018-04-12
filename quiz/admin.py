from django.contrib import admin

from django.utils.html import format_html

from .models import Unit, Choice, Question

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class UnitInline(admin.TabularInline):
    model = Unit

admin.site.register(Unit)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('escaped_question_text', 'question_unit_name', 'unit_id', 'pub_date', 'was_published_recently')

    list_filter = ['pub_date', 'unit_id']

    # actions = [change_unit]

    def escaped_question_text(self, obj):
        return format_html(obj.question_text)

    def question_unit_name(self, obj):
        return Unit.objects.get(pk=obj.unit_id)

    escaped_question_text.allow_tags = True
    escaped_question_text.short_description = 'Question text'
    
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Question Hint', {'fields': ['question_hint'], 'classes': ['']}), # put "collapse" in classes to auto-hide it; requires bootstrap
        ('Unit / Course Information', {'fields': [ 'unit'], 'classes': ['']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['']}),
    ]
    inlines = [ChoiceInline]
    search_fields = ['question_text', 'question_unit_name' ]

admin.site.register(Question, QuestionAdmin)
