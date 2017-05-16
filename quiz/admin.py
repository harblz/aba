from django.contrib import admin

from .models import Choice, Question

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'unit_name', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Question Hint', {'fields': ['question_hint'], 'classes': ['collapse']}),
        ('Unit / Course Information', {'fields': ['unit_name'], 'classes': ['collapse']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date', 'unit_name']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
