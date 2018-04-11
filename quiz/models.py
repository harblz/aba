import datetime

from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible # only if you need to support Python 2
class Unit(models.Model):
    unit_name           = models.CharField(max_length=50)
    unit_description    = models.TextField()

    def __str__(self):
        return self.unit_name

    def get_unit_description(self):
        return self.unit_description
        
    def get_unit_id(self):
        return self.unit_id

@python_2_unicode_compatible  # only if you need to support Python 2
class Question(models.Model):
    question_text   = RichTextField()
    unit            = models.ForeignKey(Unit, on_delete=models.CASCADE)
    question_hint   = RichTextField()
    pub_date        = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def get_unit_id(self):
        return self.unit_id

    get_unit_id.admin_order_field = 'Quiz ID'
    get_unit_id.short_description = 'A unique number for each quiz. Each question that belongs to the same quiz will have the same Quiz ID.'

    def get_hint(self):
        return self.question_hint
    get_hint.short_description = 'Question Hint'

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'



@python_2_unicode_compatible  # only if you need to support Python 2
class Choice(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes       = models.IntegerField(default=0)
    is_correct  = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text
