from django.contrib import admin

from django.utils.html import format_html

from django.contrib.admin import SimpleListFilter

from .models import Unit, Deck, Difficulty, Choice, Flashcard, Task

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

# Extending SimpleListFilter

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class UnitInline(admin.TabularInline):
    model = Unit
admin.site.register(Unit)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'escaped_choice_text', 'votes', 'is_correct', 'flashcard_id')
    list_per_page = 100000
    list_filter = ('flashcard_id',)

    def escaped_choice_text(self, obj):
        return format_html(obj.choice_text)
    
    escaped_choice_text.short_description = 'Flashcard text'

    search_fields = [  'choice_text' ]

admin.site.register(Choice, ChoiceAdmin)



class DeckAdmin(admin.ModelAdmin):
    list_display = ['deck_name', 'deck_short_name', 'deck_unit_id', 'deck_description']
    list_per_page = 100000
    list_filter  = ['deck_name', 'deck_unit_id']
    search_fields = [  'deck_name', 'deck_description' ]

admin.site.register(Deck, DeckAdmin)


class TaskInline(admin.TabularInline):
    model = Task
admin.site.register(Task)


class DifficultyInline(admin.TabularInline):
    model = Difficulty
admin.site.register(Difficulty)


def change_difficulty_RBT(modeladmin, request, queryset):
    queryset.update(difficulty='RBT')
change_difficulty_RBT.short_description = "Change selected flashcards difficulty to RBT"


class FlashcardAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'escaped_flashcard_text', 'flashcard_unit_name', 'flashcard_deck_name', 'has_answer', 'error_reports', 'flashcard_difficulty', 'task_list_item', 'pub_date', 'was_published_recently')
    list_per_page = 100000
    list_filter = ('unit_id', 'task_list_item', 'deck_id', 'pub_date')
    #list_filter = ('unit_id', RelatedDropdownFilter) # https://github.com/mrts/django-admin-list-filter-dropdown/issues/5

    # actions = [change_unit]

    def escaped_flashcard_text(self, obj):
        return format_html(obj.flashcard_text)

    def flashcard_unit_name(self, obj):
        return Unit.objects.get(pk=obj.unit_id)

    def flashcard_deck_name(self, obj):
        return Deck.objects.get(pk=obj.deck_id)

    def has_answer(self, obj):
        choices = Choice.objects.filter(flashcard_id=obj.id)
        status  = False;

        for choice in choices:
            if choice.is_correct is True:
                status = True;
        
        return status;

    def flashcard_difficulty(self, obj):
        return Difficulty.objects.get(pk=obj.difficulty_id)

    def task_name(self, obj):
        return Task.objects.get(pk=obj.task_list_item)

    escaped_flashcard_text.allow_tags = True
    
    escaped_flashcard_text.short_description = 'Flashcard text'

    flashcard_deck_name.short_description    = 'deck'
    flashcard_deck_name.admin_order_field    = 'deck__deck_name'

    flashcard_unit_name.short_description    = 'Unit'
    flashcard_unit_name.admin_order_field    = 'unit__unit_name'

    flashcard_difficulty.short_description   = 'Difficulty'


    has_answer.admin_order_field            = 'choice__is_correct'
    flashcard_difficulty.admin_order_field   = 'difficulty__difficulty_name'
    
    fieldsets = [
        (None,               {'fields': ['flashcard_text', 'task_list_item']}),
        ('Flashcard Hint', {'fields': ['flashcard_hint'], 'classes': ['']}), # put "collapse" in classes to auto-hide it; requires bootstrap
        ('Unit / Course Information', {'fields': [ 'unit', 'deck' ], 'classes': ['']}),
        ('Difficulty', {'fields': [ 'difficulty'], 'classes': ['']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['']}),
    ]
    inlines = [ChoiceInline]
    search_fields = [ 'id', 'flashcard_text', 'choice__choice_text', 'flashcard_hint']
admin.site.register(Flashcard, FlashcardAdmin)
