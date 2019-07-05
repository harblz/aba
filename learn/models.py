import datetime
from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from django.utils.encoding import python_2_unicode_compatible

from quiz.models import Unit, Form, Choice, Question, Task, QuizScore


# Create your models here.
class Course(models.Model):
    course_name           = models.CharField(max_length=50)
    course_description    = RichTextField()
    course_target         = models.CharField(max_length=50, default='RBT')
    course_units         = models.ManyToManyField(Unit)

    def __str__(self):
        return self.course_name

    def get_course_description(self):
        return self.course_description
        
    def get_course_id(self):
        return self.course_id


class Objective(models.Model):
    objective_name           = models.CharField(max_length=75, default='A')
    objective_short_name     = models.CharField(max_length=75, blank=True, null=True)
    objective_description    = RichTextField(null=True)
    objective_unit           = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # objective_task_list_item = models.ForeignKey(Task, on_delete=models.CASCADE)
    objective_task_list_item = models.ManyToManyField(Task)


    def __str__(self):
        return self.objective_name

    def get_objective_unit(self):
        return self.objective_unit

    def get_objective_name(self):
        return self.objective_name
        
    def get_objective_id(self):
        return self.objective_id


class LessonPage(models.Model):
    author              = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    title               = models.CharField(max_length=200)
    body                = RichTextField()
    order               = models.IntegerField()
    lesson_objectives   = models.ManyToManyField(Objective)

    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    page_views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Lesson Pages"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class Unit(models.Model):
    unit_name           = models.CharField(max_length=50)
    unit_order          = models.IntegerField(blank=True, null=True)
    unit_description    = RichTextField()
    unit_target         = models.CharField(max_length=50, default='RBT')
    unit_lessons        = models.ManyToManyField(LessonPage)

    def __str__(self):
        return self.unit_name

    def get_unit_description(self):
        return self.unit_description
        
    def get_unit_id(self):
        return self.unit_id


class TaskListItemCategory(models.Model):
    task_list_item_category_name           = models.CharField(max_length=50)
    task_list_item_category_description    = RichTextField()

    def __str__(self):
        return self.task_list_item_category_name

    def get_task_list_item_category_description(self):
        return self.task_list_item_category_description
        
    def get_task_list_item_category_id(self):
        return self.task_list_item_category_id

class TaskListItem(models.Model):
    task_list_item_name           = models.CharField(max_length=50)
    task_list_item_description    = RichTextField()

    def __str__(self):
        return self.task_list_item_name

    def get_task_list_item_description(self):
        return self.task_list_item_description
        
    def get_task_list_item_id(self):
        return self.task_list_item_id


class Certification(models.Model):
    certification_name           = models.CharField(max_length=50)
    certification_description    = RichTextField()

    def __str__(self):
        return self.certification_name

    def get_certification_description(self):
        return self.certification_description
        
    def get_certification_id(self):
        return self.certification_id