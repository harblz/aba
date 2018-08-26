import datetime
from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from django.utils.encoding import python_2_unicode_compatible


class Unit(models.Model):
    unit_name           = models.CharField(max_length=50)
    unit_description    = RichTextField()
    unit_target         = models.CharField(max_length=50, default='RBT')

    def __str__(self):
        return self.unit_name

    def get_unit_description(self):
        return self.unit_description
        
    def get_unit_id(self):
        return self.unit_id


class Form(models.Model):
    form_name           = models.CharField(max_length=50, default='A')
    form_description    = RichTextField(null=True)
    form_unit           = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.form_name

    def get_form_unit(self):
        return self.form_unit

    def get_form_name(self):
        return self.form_name
        
    def get_form_id(self):
        return self.form_id


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
    task_version            = models.CharField(max_length=50, default='2017')    

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

 
class Question(models.Model):
    question_text   = RichTextField()
    unit            = models.ForeignKey(Unit, on_delete=models.CASCADE)
    form            = models.ForeignKey(Form, on_delete=models.CASCADE)
    task_list_item  = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    difficulty      = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    question_hint   = RichTextField()
    pub_date        = models.DateTimeField('date published')


    def __str__(self):
        return self.question_text

    def get_unit_id(self):
        return self.unit_id

    def get_difficulty_id(self):
        return self.difficulty_id

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



 
class Choice(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = RichTextField()
    votes       = models.IntegerField(default=0)
    is_correct  = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text
