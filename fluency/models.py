import datetime
from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from django.utils.encoding import python_2_unicode_compatible

class Unit(models.Model):
    unit_name           = models.CharField(max_length=50)
    unit_description    = RichTextField()
    unit_target         = models.CharField(max_length=50, default='BCBA')

    def __str__(self):
        return self.unit_name

    def get_unit_description(self):
        return self.unit_description
        
    def get_unit_id(self):
        return self.unit_id


class Deck(models.Model):
    deck_name           = models.CharField(max_length=75, default='1')
    deck_short_name     = models.CharField(max_length=75, blank=True, null=True)
    deck_description    = RichTextField(null=True)
    deck_unit           = models.ForeignKey(Unit, on_delete=models.CASCADE)
    deck_timed_duration = models.IntegerField(default=60)

    def __str__(self):
        return self.deck_name

    def get_deck_unit(self):
        return self.deck_unit

    def get_deck_name(self):
        return self.deck_name
        
    def get_deck_id(self):
        return self.deck_id


class Difficulty(models.Model):
    difficulty_name         = models.CharField(max_length=25)
    difficulty_description  = RichTextField()

    class Meta:
        verbose_name_plural = "Difficulties"

    def __str__(self):
        return self.difficulty_name

    def get_difficulty_description(self):
        return self.difficulty_description
        
    def get_difficulty_id(self):
        return self.difficulty_id


class Task(models.Model):
    task_name               = models.CharField(max_length=50)
    task_list_description   = RichTextField()
    certification           = models.CharField(max_length=25, default='RBT')
    task_version            = models.CharField(max_length=50, default='2019')    

    def __str__(self):
        return self.task_name

    def get_task_name(self):
        return self.task_name

    def get_task_description(self):
        return self.task_description

    def get_task_certification(self):
        return self.task_certification

    def get_task_version(self):
        return self.task_version

    def get_task_id(self):
        return self.task_id


class FluencyUntimedScore(models.Model):
    id              = models.AutoField(primary_key=True, editable=False)
    score           = models.DecimalField(blank=True, null=True, decimal_places=3,max_digits=5)
    unit_id         = models.ForeignKey(Unit, on_delete=models.CASCADE)
    deck_id         = models.ForeignKey(Deck, on_delete=models.CASCADE)
    date            = models.DateTimeField()


class FluencyUntimedScoreSummary(FluencyUntimedScore):
    class Meta:
        proxy = True
        verbose_name = 'Fluency Untimed Score Summary'
        verbose_name_plural = 'Fluency Untimed Scores Summary'


class FluencyTimedScore(models.Model):
    id              = models.AutoField(primary_key=True, editable=False)
    score           = models.DecimalField(blank=True, null=True, decimal_places=3,max_digits=5)
    time_elapsed    = models.IntegerField(blank=True, null=True) # time elapsed to complete quiz in seconds
    unit_id         = models.ForeignKey(Unit, on_delete=models.CASCADE)
    deck_id         = models.ForeignKey(Deck, on_delete=models.CASCADE)
    date            = models.DateTimeField()



class FluencyTimedScoreSummary(FluencyTimedScore):
    class Meta:
        proxy = True
        verbose_name = 'Fluency Timed Score Summary'
        verbose_name_plural = 'Fluency Timed Scores Summary'


class Flashcard(models.Model):
    id                  = models.AutoField(primary_key=True, editable=False)
    flashcard_text      = RichTextField()
    unit                = models.ForeignKey(Unit, on_delete=models.CASCADE)
    deck                = models.ForeignKey(Deck, on_delete=models.CASCADE)
    task_list_item      = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    task_list_data      = models.CharField(default=None, max_length=50, null=True)
    difficulty          = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    flashcard_hint      = RichTextField()
    pub_date            = models.DateTimeField('date published')
    flashcard_choices   = models.CharField(default=None, max_length=50, null=True)
    error_reports       = models.IntegerField(default=0)


    def __str__(self):
        return self.flashcard_text

    def flashcard_id(self):
        return self.id

    def get_unit_id(self):
        return self.unit_id

    def get_difficulty_id(self):
        return self.difficulty_id

    get_unit_id.admin_order_field = 'Quiz ID'
    get_unit_id.short_description = 'A unique number for each quiz. Each Flashcard that belongs to the same quiz will have the same Quiz ID.'

    def get_hint(self):
        return self.flashcard_hint
    get_hint.short_description = 'Flashcard Hint'

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    flashcard   = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    choice_text = RichTextField()
    votes       = models.IntegerField(default=0)
    is_correct  = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text
