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

    def __str__(self):
        return self.course_name

    def get_course_description(self):
        return self.course_description
        
    def get_course_id(self):
        return self.course_id